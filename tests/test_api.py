import pytest
import os
import sys
import json
from unittest.mock import patch, MagicMock

# Add the parent directory to the path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the Flask app
import api


@pytest.fixture
def client():
    """Create a test client for the Flask app"""
    api.app.config['TESTING'] = True
    with api.app.test_client() as client:
        yield client


@pytest.fixture
def mock_flight_data():
    """Set up mock for the FlightData class"""
    with patch('api.FlightData') as MockFlightData:
        mock_instance = MockFlightData.return_value
        api.flight_data = mock_instance
        yield mock_instance


def test_index(client):
    """Test the index route"""
    response = client.get('/')
    data = json.loads(response.data)

    assert response.status_code == 200
    assert 'name' in data
    assert 'endpoints' in data
    assert len(data['endpoints']) > 0


def test_get_flight_by_id_found(client, mock_flight_data):
    """Test getting a flight by ID when it exists"""
    # Set up mock to return a flight
    mock_flight_data.get_flight_by_id.return_value = [
        {"ID": 12345, "ORIGIN_AIRPORT": "LAX", "DESTINATION_AIRPORT": "JFK", "AIRLINE": "Delta", "DELAY": 0}
    ]

    # Make the request
    response = client.get('/api/flights/12345')
    data = json.loads(response.data)

    # Check the response
    assert response.status_code == 200
    assert data['success'] is True
    assert len(data['data']) == 1
    assert data['data'][0]['ID'] == 12345

    # Verify the mock was called correctly
    mock_flight_data.get_flight_by_id.assert_called_once_with(12345)


def test_get_flight_by_id_not_found(client, mock_flight_data):
    """Test getting a flight by ID when it doesn't exist"""
    # Set up mock to return empty list
    mock_flight_data.get_flight_by_id.return_value = []

    # Make the request
    response = client.get('/api/flights/99999')
    data = json.loads(response.data)

    # Check the response
    assert response.status_code == 400
    assert data['success'] is False
    assert 'error' in data

    # Verify the mock was called correctly
    mock_flight_data.get_flight_by_id.assert_called_once_with(99999)


def test_get_flights_by_date(client, mock_flight_data):
    """Test getting flights by date"""
    # Set up mock to return flights
    mock_flight_data.get_flights_by_date.return_value = [
        {"ID": 1, "ORIGIN_AIRPORT": "LAX", "DESTINATION_AIRPORT": "JFK", "AIRLINE": "Delta"},
        {"ID": 2, "ORIGIN_AIRPORT": "SFO", "DESTINATION_AIRPORT": "ORD", "AIRLINE": "United"}
    ]

    # Make the request
    response = client.get('/api/flights/date/2023/6/15')
    data = json.loads(response.data)

    # Check the response
    assert response.status_code == 200
    assert data['success'] is True
    assert len(data['data']) == 2

    # Verify the mock was called correctly
    mock_flight_data.get_flights_by_date.assert_called_once_with(15, 6, 2023)


def test_get_flights_by_date_invalid(client):
    """Test input validation for invalid date"""
    # Make the request with invalid month
    response = client.get('/api/flights/date/2023/13/15')
    data = json.loads(response.data)

    # Check the response
    assert response.status_code == 400
    assert data['success'] is False
    assert 'error' in data


def test_get_flights_by_origin(client, mock_flight_data):
    """Test getting flights by origin airport"""
    # Set up mock to return flights
    mock_flight_data.get_flights_by_origin.return_value = [
        {"ID": 1, "ORIGIN_AIRPORT": "LAX", "DESTINATION_AIRPORT": "JFK", "AIRLINE": "Delta"},
        {"ID": 2, "ORIGIN_AIRPORT": "LAX", "DESTINATION_AIRPORT": "ORD", "AIRLINE": "United"}
    ]

    # Make the request
    response = client.get('/api/flights/origin/LAX')
    data = json.loads(response.data)

    # Check the response
    assert response.status_code == 200
    assert data['success'] is True
    assert len(data['data']) == 2
    assert data['data'][0]['ORIGIN_AIRPORT'] == 'LAX'

    # Verify the mock was called correctly with uppercase IATA code
    mock_flight_data.get_flights_by_origin.assert_called_once_with('LAX')


def test_get_airline_stats(client, mock_flight_data):
    """Test getting airline statistics"""
    # Set up mocks to return airline data
    mock_flight_data.get_delayed_flights_by_airline.return_value = [
        {"airline": "Delta", "delayed_flights": 150},
        {"airline": "United", "delayed_flights": 200}
    ]
    mock_flight_data.get_total_flights_by_airline.return_value = [
        {"airline": "Delta", "total_flights": 1000},
        {"airline": "United", "total_flights": 1200}
    ]

    # Make the request
    response = client.get('/api/stats/airlines')
    data = json.loads(response.data)

    # Check the response
    assert response.status_code == 200
    assert data['success'] is True
    assert len(data['data']) == 2

    # Check that percentages were calculated correctly
    delta_stats = next(item for item in data['data'] if item['airline'] == 'Delta')
    assert delta_stats['percentage_delayed'] == 15.0  # 150/1000 * 100

    united_stats = next(item for item in data['data'] if item['airline'] == 'United')
    assert united_stats['percentage_delayed'] == 16.67  # 200/1200 * 100, rounded to 2 decimal places