from sqlalchemy import create_engine, text

# Constants
DELAY_THRESHOLD = 20

# Query definitions
QUERY_FLIGHT_BY_ID = """
SELECT flights.ID as id, flights.YEAR as year, flights.MONTH as month, flights.DAY as day, 
       flights.ORIGIN_AIRPORT as origin_airport, flights.DESTINATION_AIRPORT as destination_airport, 
       airlines.airline as airline_name, flights.DEPARTURE_DELAY as delay
FROM flights 
JOIN airlines ON flights.airline = airlines.id 
WHERE flights.ID = :id
"""

QUERY_DELAYED_FLIGHTS = f"""
SELECT flights.ID as id, flights.FLIGHT_NUMBER as flight_number, 
       flights.ORIGIN_AIRPORT as origin_airport, flights.DESTINATION_AIRPORT as destination_airport,
       airlines.airline as airline_name, flights.DEPARTURE_DELAY as delay
FROM flights 
JOIN airlines ON flights.airline = airlines.id 
WHERE flights.DEPARTURE_DELAY >= {DELAY_THRESHOLD}
ORDER BY airlines.airline, flights.DEPARTURE_DELAY DESC
"""

QUERY_DELAYED_FLIGHTS_BY_AIRLINE = f"""
SELECT flights.ID as id, flights.FLIGHT_NUMBER as flight_number, 
       flights.ORIGIN_AIRPORT as origin_airport, flights.DESTINATION_AIRPORT as destination_airport,
       airlines.airline as airline_name, flights.DEPARTURE_DELAY as delay
FROM flights 
JOIN airlines ON flights.airline = airlines.id 
WHERE flights.DEPARTURE_DELAY >= {DELAY_THRESHOLD}
AND airlines.airline = :airline_name
ORDER BY flights.DEPARTURE_DELAY DESC
"""

QUERY_TOTAL_FLIGHTS_BY_AIRLINE = """
SELECT airlines.airline, COUNT(*) as total_flights 
FROM flights 
JOIN airlines ON flights.airline = airlines.id 
GROUP BY airlines.airline
"""

QUERY_DELAYED_FLIGHTS_BY_HOUR = f"""
SELECT CAST(SUBSTR(DEPARTURE_TIME, 1, 2) AS INTEGER) AS hour, COUNT(*) as delayed_flights 
FROM flights 
WHERE DEPARTURE_DELAY >= {DELAY_THRESHOLD} 
GROUP BY hour 
ORDER BY hour
"""

QUERY_TOTAL_FLIGHTS_BY_HOUR = """
SELECT CAST(SUBSTR(DEPARTURE_TIME, 1, 2) AS INTEGER) AS hour, COUNT(*) as total_flights 
FROM flights 
GROUP BY hour 
ORDER BY hour
"""

QUERY_DELAYED_FLIGHTS_BY_ROUTE = f"""
SELECT ORIGIN_AIRPORT, DESTINATION_AIRPORT, COUNT(*) as delayed_flights 
FROM flights 
WHERE DEPARTURE_DELAY >= {DELAY_THRESHOLD} 
GROUP BY ORIGIN_AIRPORT, DESTINATION_AIRPORT
"""

QUERY_TOTAL_FLIGHTS_BY_ROUTE = """
SELECT ORIGIN_AIRPORT, DESTINATION_AIRPORT, COUNT(*) as total_flights 
FROM flights 
GROUP BY ORIGIN_AIRPORT, DESTINATION_AIRPORT
"""

QUERY_FLIGHTS_BY_ORIGIN = f"""
SELECT flights.ID as id, flights.ORIGIN_AIRPORT as origin_airport, flights.DESTINATION_AIRPORT as destination_airport, 
       airlines.airline as airline_name, flights.DEPARTURE_DELAY as delay
FROM flights 
JOIN airlines ON flights.airline = airlines.id 
WHERE flights.ORIGIN_AIRPORT = :origin
  AND flights.DEPARTURE_DELAY IS NOT NULL
  AND flights.DEPARTURE_DELAY >= {DELAY_THRESHOLD}
"""

QUERY_FLIGHTS_BY_DATE = """
SELECT flights.ID as id, flights.YEAR as year, flights.MONTH as month, flights.DAY as day, 
       flights.ORIGIN_AIRPORT as origin_airport, flights.DESTINATION_AIRPORT as destination_airport, 
       airlines.airline as airline_name, flights.DEPARTURE_DELAY as delay
FROM flights 
JOIN airlines ON flights.airline = airlines.id 
WHERE flights.DAY = :day AND flights.MONTH = :month AND flights.YEAR = :year
"""

QUERY_TOP_5_DELAYED_FLIGHTS_BY_DATE = """
SELECT flights.ID as id, flights.FLIGHT_NUMBER as flight_number, flights.ORIGIN_AIRPORT as origin, flights.DEPARTURE_DELAY as delay
FROM flights
WHERE flights.DEPARTURE_DELAY IS NOT NULL
  AND flights.DEPARTURE_DELAY > 0
  AND flights.DAY = :day
  AND flights.MONTH = :month
  AND flights.YEAR = :year
ORDER BY flights.DEPARTURE_DELAY DESC
LIMIT :limit
"""


class FlightData:
    def __init__(self, uri):
        self.engine = create_engine(uri)

    def _execute_query(self, query, params=None):
        if params is None:
            params = {}
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query), parameters=params)
                rows = [dict(row._mapping) for row in result]
                # Lowercase keys immediately
                return [{k.lower(): v for k, v in row.items()} for row in rows]
        except Exception as e:
            print(f"Database query failed: {e}")
            return []

    def get_flight_by_id(self, flight_id):
        return self._execute_query(QUERY_FLIGHT_BY_ID, {"id": flight_id})

    def get_flights_by_date(self, day, month, year):
        return self._execute_query(QUERY_FLIGHTS_BY_DATE, {"day": day, "month": month, "year": year})

    def get_delayed_flights_by_airline(self, airline_name=None):
        if airline_name:
            return self._execute_query(QUERY_DELAYED_FLIGHTS_BY_AIRLINE, {"airline_name": airline_name})
        else:
            return self._execute_query(QUERY_DELAYED_FLIGHTS)

    def get_delayed_flights_by_airport(self, airport_code):
        return self._execute_query(QUERY_FLIGHTS_BY_ORIGIN, {"origin": airport_code})

    def get_top_delayed_flights_by_date(self, day, month, year, limit=5):
        return self._execute_query(
            QUERY_TOP_5_DELAYED_FLIGHTS_BY_DATE, 
            {"day": day, "month": month, "year": year, "limit": limit}
        )

    def get_delayed_flights(self):
        return self._execute_query(QUERY_DELAYED_FLIGHTS)

    def get_total_flights_by_airline(self):
        return self._execute_query(QUERY_TOTAL_FLIGHTS_BY_AIRLINE)

    def get_delayed_flights_by_hour(self):
        return self._execute_query(QUERY_DELAYED_FLIGHTS_BY_HOUR)

    def get_total_flights_by_hour(self):
        return self._execute_query(QUERY_TOTAL_FLIGHTS_BY_HOUR)

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
