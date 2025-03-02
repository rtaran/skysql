import pytest
import os
import sys
from unittest.mock import patch, MagicMock

# Add the parent directory to the path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data import FlightData

# Mock database URI for testing
TEST_DB_URI = "sqlite:///:memory:"


class TestFlightData:
    @pytest.fixture
    def data_manager(self):
        """Create a FlightData instance with a mocked engine"""
        with patch('data.create_engine') as mock_create_engine:
            mock_engine = MagicMock()
            mock_create_engine.return_value = mock_engine
            data_manager = FlightData(TEST_DB_URI)
            # Set up the mock to return expected results
            mock_connection = MagicMock()
            mock_engine.connect.return_value.__enter__.return_value = mock_connection
            data_manager._mock_connection = mock_connection
            yield data_manager

    def test_get_flight_by_id(self, data_manager):
        """Test retrieving a flight by ID"""
        # Setup the mock to return a specific result
        mock_result = MagicMock()
        mock_result.__iter__.return_value = [
            {"ID": 1, "ORIGIN_AIRPORT": "LAX", "DESTINATION_AIRPORT": "JFK", "AIRLINE": "Delta", "DELAY": 15}]
        data_manager._mock_connection.execute.return_value = mock_result

        # Call the method
        result = data_manager.get_flight_by_id(1)

        # Verify the result
        assert len(result) == 1
        assert result[0]["ID"] == 1
        assert result[0]["ORIGIN_AIRPORT"] == "LAX"

        # Verify the correct query was executed
        call_args = data_manager._mock_connection.execute.call_args[0]
        assert "WHERE flights.ID = :id" in str(call_args[0])

    def test_get_delayed_flights(self, data_manager):
        """Test retrieving delayed flights"""
        # Setup the mock to return specific results
        mock_result = MagicMock()
        mock_result.__iter__.return_value = [
            {"ID": 1, "ORIGIN_AIRPORT": "LAX", "DESTINATION_AIRPORT": "JFK", "AIRLINE": "Delta", "DEPARTURE_DELAY": 25},
            {"ID": 2, "ORIGIN_AIRPORT": "SFO", "DESTINATION_AIRPORT": "ORD", "AIRLINE": "United", "DEPARTURE_DELAY": 30}
        ]
        data_manager._mock_connection.execute.return_value = mock_result

        # Call the method
        result = data_manager.get_delayed_flights()

        # Verify the result
        assert len(result) == 2
        assert result[0]["DEPARTURE_DELAY"] == 25
        assert result[1]["DEPARTURE_DELAY"] == 30

        # Verify the correct query was executed
        call_args = data_manager._mock_connection.execute.call_args[0]
        assert "WHERE flights.DEPARTURE_DELAY >= 20" in str(call_args[0])

    def test_get_flights_by_origin_invalid_code(self, data_manager):
        """Test input validation for invalid IATA code"""
        result = data_manager.get_flights_by_origin("INVALID")
        assert result == []

        result = data_manager.get_flights_by_origin(123)
        assert result == []

    def test_get_flights_by_origin_valid_code(self, data_manager):
        """Test retrieving flights by origin with valid IATA code"""
        # Setup the mock to return specific results
        mock_result = MagicMock()
        mock_result.__iter__.return_value = [
            {"ID": 1, "ORIGIN_AIRPORT": "LAX", "DESTINATION_AIRPORT": "JFK", "AIRLINE": "Delta"}
        ]
        data_manager._mock_connection.execute.return_value = mock_result

        # Call the method
        result = data_manager.get_flights_by_origin("LAX")

        # Verify the result
        assert len(result) == 1
        assert result[0]["ORIGIN_AIRPORT"] == "LAX"

        # Verify the correct query was executed with uppercase IATA code
        call_args = data_manager._mock_connection.execute.call_args[0]
        assert "WHERE flights.ORIGIN_AIRPORT = :origin" in str(call_args[0])
        call_kwargs = data_manager._mock_connection.execute.call_args[1]
        assert call_kwargs["params"]["origin"] == "LAX"

    def test_get_delayed_flights_by_airline(self, data_manager):
        """Test retrieving delayed flights by airline"""
        # Setup the mock to return specific results
        mock_result = MagicMock()
        mock_result.__iter__.return_value = [
            {"airline": "Delta", "delayed_flights": 150}
        ]
        data_manager._mock_connection.execute.return_value = mock_result

        # Call the method
        result = data_manager.get_delayed_flights_by_airline("Delta")

        # Verify the result
        assert len(result) == 1
        assert result[0]["airline"] == "Delta"
        assert result[0]["delayed_flights"] == 150