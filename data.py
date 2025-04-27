import sqlalchemy
from sqlalchemy import create_engine, text

# Query definitions
QUERY_FLIGHT_BY_ID = """
SELECT flights.*, airlines.airline, flights.ID as FLIGHT_ID, flights.DEPARTURE_DELAY as DELAY 
FROM flights 
JOIN airlines ON flights.airline = airlines.id 
WHERE flights.ID = :id
"""

QUERY_DELAYED_FLIGHTS = """
SELECT airlines.airline, COUNT(*) as delayed_flights 
FROM flights 
JOIN airlines ON flights.airline = airlines.id 
WHERE flights.DEPARTURE_DELAY >= 20 
GROUP BY airlines.airline
"""

QUERY_DELAYED_FLIGHTS_BY_AIRLINE = """
SELECT airlines.airline, COUNT(*) as delayed_flights 
FROM flights 
JOIN airlines ON flights.airline = airlines.id 
WHERE flights.DEPARTURE_DELAY >= 20 
GROUP BY airlines.airline
"""

QUERY_TOTAL_FLIGHTS_BY_AIRLINE = """
SELECT airlines.airline, COUNT(*) as total_flights 
FROM flights 
JOIN airlines ON flights.airline = airlines.id 
GROUP BY airlines.airline
"""

QUERY_DELAYED_FLIGHTS_BY_HOUR = """
SELECT CAST(SUBSTR(DEPARTURE_TIME, 1, 2) AS INTEGER) AS hour, COUNT(*) as delayed_flights 
FROM flights 
WHERE DEPARTURE_DELAY >= 20 
GROUP BY hour 
ORDER BY hour
"""

QUERY_TOTAL_FLIGHTS_BY_HOUR = """
SELECT CAST(SUBSTR(DEPARTURE_TIME, 1, 2) AS INTEGER) AS hour, COUNT(*) as total_flights 
FROM flights 
GROUP BY hour 
ORDER BY hour
"""

QUERY_DELAYED_FLIGHTS_BY_ROUTE = """
SELECT ORIGIN_AIRPORT, DESTINATION_AIRPORT, COUNT(*) as delayed_flights 
FROM flights 
WHERE DEPARTURE_DELAY >= 20 
GROUP BY ORIGIN_AIRPORT, DESTINATION_AIRPORT
"""

QUERY_TOTAL_FLIGHTS_BY_ROUTE = """
SELECT ORIGIN_AIRPORT, DESTINATION_AIRPORT, COUNT(*) as total_flights 
FROM flights 
GROUP BY ORIGIN_AIRPORT, DESTINATION_AIRPORT
"""

QUERY_FLIGHTS_BY_ORIGIN = """
SELECT flights.*, airlines.airline 
FROM flights 
JOIN airlines ON flights.airline = airlines.id 
WHERE flights.ORIGIN_AIRPORT = :origin
"""

QUERY_FLIGHTS_BY_DESTINATION = """
SELECT flights.*, airlines.airline 
FROM flights 
JOIN airlines ON flights.airline = airlines.id 
WHERE flights.DESTINATION_AIRPORT = :destination
"""

QUERY_FLIGHTS_BY_DATE = """
SELECT flights.*, airlines.airline 
FROM flights 
JOIN airlines ON flights.airline = airlines.id 
WHERE flights.DAY = :day AND flights.MONTH = :month AND flights.YEAR = :year
"""

QUERY_DELAYED_FLIGHTS_BY_AIRPORT = """
SELECT flights.*, airlines.airline 
FROM flights 
JOIN airlines ON flights.airline = airlines.id 
WHERE flights.ORIGIN_AIRPORT = :origin
  AND flights.DEPARTURE_DELAY IS NOT NULL
  AND flights.DEPARTURE_DELAY >= 0
"""

QUERY_TOP_5_DELAYED_FLIGHTS_BY_DATE = """
SELECT flights.*, airlines.airline, flights.DEPARTURE_DELAY
FROM flights
JOIN airlines ON flights.airline = airlines.id
WHERE flights.DEPARTURE_DELAY IS NOT NULL
  AND flights.DEPARTURE_DELAY > 0
  AND flights.DAY = :day
  AND flights.MONTH = :month
  AND flights.YEAR = :year
ORDER BY flights.DEPARTURE_DELAY DESC
LIMIT :limit
"""


class FlightData:
    """
    The FlightData class is a Data Access Layer (DAL) object that provides an
    interface to the flight data in the SQLITE database.
    """

    def __init__(self, uri):
        self.engine = create_engine(uri)

    def _execute_query(self, query, params=None):
        """
        Execute an SQL query with the params provided in a dictionary,
        and return a list of records (dictionary-like objects).
        If an exception was raised, print the error, and return an empty list.
        Uses a mock connection if _mock_connection is set (for testing).
        """
        if params is None:
            params = {}
        try:
            connection = getattr(self, "_mock_connection", None)
            if connection is not None:
                result = connection.execute(text(query), parameters=params)
                return [dict(row) for row in result]
            with self.engine.connect() as conn:
                result = conn.execute(text(query), parameters=params)
                return [dict(row._mapping) for row in result]
        except Exception as e:
            print(f"Database query failed: {e}")
            return []

    def get_flight_by_id(self, flight_id):
        return _lowercase_mapping_rows(self._execute_query(QUERY_FLIGHT_BY_ID, {"id": flight_id}))

    def get_flights_by_date(self, day, month, year):
        return _lowercase_mapping_rows(self._execute_query(QUERY_FLIGHTS_BY_DATE, {"day": day, "month": month, "year": year}))

    def get_delayed_flights_by_airline(self, airline=None):
        if airline:
            query = """
            SELECT airlines.airline AS airline, COUNT(*) AS delayed_flights
            FROM flights
            JOIN airlines ON flights.airline = airlines.id
            WHERE airlines.airline = :airline AND flights.DEPARTURE_DELAY >= 20
            GROUP BY airlines.airline
            """
            params = {"airline": airline}
        else:
            query = QUERY_DELAYED_FLIGHTS_BY_AIRLINE
            params = None
        rows = self._execute_query(query, params) if params else self._execute_query(query)
        return [{k.lower(): v for k, v in row.items()} for row in rows]

    def get_delayed_flights_by_airport(self, airport_code):
        return _lowercase_mapping_rows(self._execute_query(QUERY_DELAYED_FLIGHTS_BY_AIRPORT, {"origin": airport_code}))

    def get_top_delayed_flights_by_date(self, day, month, year, limit=5):
        return _lowercase_mapping_rows(self._execute_query(QUERY_TOP_5_DELAYED_FLIGHTS_BY_DATE, {
            "day": day, "month": month, "year": year, "limit": limit
        }))

    def get_delayed_flights(self):
        return self._execute_query(QUERY_DELAYED_FLIGHTS)

    def get_flights_by_origin(self, origin):
        if not isinstance(origin, str) or len(origin) != 3 or not origin.isalpha():
            print("Invalid IATA code. Please enter a valid 3-letter airport code.")
            return []
        params = {'origin': origin.upper()}
        return self._execute_query(QUERY_FLIGHTS_BY_ORIGIN, params)

    def get_flights_by_destination(self, destination):
        params = {'destination': destination}
        return self._execute_query(QUERY_FLIGHTS_BY_DESTINATION, params)

    def get_total_flights_by_airline(self):
        return _lowercase_mapping_rows(self._execute_query(QUERY_TOTAL_FLIGHTS_BY_AIRLINE))

    def get_delayed_flights_by_hour(self):
        return _lowercase_mapping_rows(self._execute_query(QUERY_DELAYED_FLIGHTS_BY_HOUR))

    def get_total_flights_by_hour(self):
        return _lowercase_mapping_rows(self._execute_query(QUERY_TOTAL_FLIGHTS_BY_HOUR))

    def get_delayed_flights_by_route(self):
        return self._execute_query(QUERY_DELAYED_FLIGHTS_BY_ROUTE)

    def get_total_flights_by_route(self):
        return self._execute_query(QUERY_TOTAL_FLIGHTS_BY_ROUTE)

    def __del__(self):
        if hasattr(self, "engine"):
            try:
                self.engine.dispose()
            except Exception:
                pass


def _lowercase_mapping_rows(results):
    """
    Convert SQLAlchemy RowMapping results to list of dicts with lowercase keys.
    """
    return [{k.lower(): v for k, v in row.items()} for row in results]