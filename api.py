import os
from flask import Flask, jsonify, request
from data import FlightData

# Create Flask app
app = Flask(__name__)

# Get the absolute path to the database file
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, "flights.sqlite3")
SQLITE_URI = f"sqlite:///{db_path}"

# Create FlightData instance
flight_data = FlightData(SQLITE_URI)


# Helper function to format JSON responses
def format_response(data, error=None):
    if error:
        return jsonify({"success": False, "error": error}), 400
    return jsonify({"success": True, "data": data}), 200


@app.route('/')
def index():
    return jsonify({
        "name": "Flights Data API",
        "version": "1.0",
        "endpoints": [
            "/api/flights/<flight_id>",
            "/api/flights/date/<year>/<month>/<day>",
            "/api/flights/delayed",
            "/api/flights/origin/<origin_code>",
            "/api/flights/destination/<destination_code>",
            "/api/flights/delayed/origin/<origin_code>",
            "/api/flights/delayed/airline/<airline_name>",
            "/api/stats/airlines",
            "/api/stats/hours",
            "/api/stats/routes"
        ]
    })


@app.route('/api/flights/<int:flight_id>')
def get_flight_by_id(flight_id):
    """Get flight details by ID"""
    results = flight_data.get_flight_by_id(flight_id)
    if not results:
        return format_response(None, f"Flight with ID {flight_id} not found")
    return format_response(results)


@app.route('/api/flights/date/<int:year>/<int:month>/<int:day>')
def get_flights_by_date(year, month, day):
    """Get flights by date"""
    # Basic date validation
    if not (1 <= month <= 12 and 1 <= day <= 31):
        return format_response(None, "Invalid date parameters")

    results = flight_data.get_flights_by_date(day, month, year)
    return format_response(results)


@app.route('/api/flights/delayed')
def get_delayed_flights():
    """Get all delayed flights"""
    results = flight_data.get_delayed_flights()
    return format_response(results)


@app.route('/api/flights/origin/<origin_code>')
def get_flights_by_origin(origin_code):
    """Get flights by origin airport"""
    if not isinstance(origin_code, str) or len(origin_code) != 3 or not origin_code.isalpha():
        return format_response(None, "Invalid IATA code. Please enter a valid 3-letter airport code.")

    results = flight_data.get_flights_by_origin(origin_code.upper())
    return format_response(results)


@app.route('/api/flights/destination/<destination_code>')
def get_flights_by_destination(destination_code):
    """Get flights by destination airport"""
    if not isinstance(destination_code, str) or len(destination_code) != 3 or not destination_code.isalpha():
        return format_response(None, "Invalid IATA code. Please enter a valid 3-letter airport code.")

    results = flight_data.get_flights_by_destination(destination_code.upper())
    return format_response(results)


@app.route('/api/flights/delayed/origin/<origin_code>')
def get_delayed_flights_by_airport(origin_code):
    """Get delayed flights by origin airport"""
    if not isinstance(origin_code, str) or len(origin_code) != 3 or not origin_code.isalpha():
        return format_response(None, "Invalid IATA code. Please enter a valid 3-letter airport code.")

    results = flight_data.get_delayed_flights_by_airport(origin_code.upper())
    return format_response(results)


@app.route('/api/flights/delayed/airline/<airline_name>')
def get_delayed_flights_by_airline(airline_name):
    """Get delayed flights by airline"""
    results = flight_data.get_delayed_flights_by_airline(airline_name)
    return format_response(results)


@app.route('/api/stats/airlines')
def get_airline_stats():
    """Get statistics on flight delays by airline"""
    delayed_data = flight_data.get_delayed_flights_by_airline()
    total_data = flight_data.get_total_flights_by_airline()

    if not delayed_data or not total_data:
        return format_response([])

    # Create a dictionary to merge data
    stats = {}

    # Process total flights data
    for row in total_data:
        airline = row.get('airline')
        if airline:
            stats[airline] = {
                'airline': airline,
                'total_flights': row.get('total_flights', 0),
                'delayed_flights': 0,
                'percentage_delayed': 0
            }

    # Process delayed flights data
    for row in delayed_data:
        airline = row.get('airline')
        if airline and airline in stats:
            stats[airline]['delayed_flights'] = row.get('delayed_flights', 0)
            # Calculate percentage
            if stats[airline]['total_flights'] > 0:
                stats[airline]['percentage_delayed'] = round(
                    (stats[airline]['delayed_flights'] / stats[airline]['total_flights']) * 100, 2
                )

    return format_response(list(stats.values()))


@app.route('/api/stats/hours')
def get_hourly_stats():
    """Get statistics on flight delays by hour of day"""
    delayed_data = flight_data.get_delayed_flights_by_hour()
    total_data = flight_data.get_total_flights_by_hour()

    if not delayed_data or not total_data:
        return format_response([])

    # Create a dictionary to merge data
    stats = {}

    # Process total flights data
    for row in total_data:
        hour = row.get('HOUR')
        if hour is not None:
            stats[hour] = {
                'hour': hour,
                'total_flights': row.get('total_flights', 0),
                'delayed_flights': 0,
                'percentage_delayed': 0
            }

    # Process delayed flights data
    for row in delayed_data:
        hour = row.get('HOUR')
        if hour is not None and hour in stats:
            stats[hour]['delayed_flights'] = row.get('delayed_flights', 0)
            # Calculate percentage
            if stats[hour]['total_flights'] > 0:
                stats[hour]['percentage_delayed'] = round(
                    (stats[hour]['delayed_flights'] / stats[hour]['total_flights']) * 100, 2
                )

    # Sort by hour for easier consumption
    return format_response(sorted(list(stats.values()), key=lambda x: x['hour']))


@app.route('/api/stats/routes')
def get_route_stats():
    """Get statistics on flight delays by route"""
    delayed_data = flight_data.get_delayed_flights_by_route()
    total_data = flight_data.get_total_flights_by_route()

    if not delayed_data or not total_data:
        return format_response([])

    # Create a dictionary to merge data using route as key
    stats = {}

    # Process total flights data
    for row in total_data:
        origin = row.get('ORIGIN_AIRPORT')
        destination = row.get('DESTINATION_AIRPORT')
        if origin and destination:
            route_key = f"{origin}-{destination}"
            stats[route_key] = {
                'origin': origin,
                'destination': destination,
                'total_flights': row.get('total_flights', 0),
                'delayed_flights': 0,
                'percentage_delayed': 0
            }

    # Process delayed flights data
    for row in delayed_data:
        origin = row.get('ORIGIN_AIRPORT')
        destination = row.get('DESTINATION_AIRPORT')
        if origin and destination:
            route_key = f"{origin}-{destination}"
            if route_key in stats:
                stats[route_key]['delayed_flights'] = row.get('delayed_flights', 0)
                # Calculate percentage
                if stats[route_key]['total_flights'] > 0:
                    stats[route_key]['percentage_delayed'] = round(
                        (stats[route_key]['delayed_flights'] / stats[route_key]['total_flights']) * 100, 2
                    )

    return format_response(list(stats.values()))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)