from sqlalchemy import create_engine, text

QUERY_FLIGHT_BY_ID = "SELECT flights.*, airlines.airline, flights.ID as FLIGHT_ID, flights.DEPARTURE_DELAY as DELAY FROM flights JOIN airlines ON flights.airline = airlines.id WHERE flights.ID = :id"
QUERY_DELAYED_FLIGHTS = "SELECT flights.*, airlines.airline FROM flights JOIN airlines ON flights.airline = airlines.id WHERE flights.DEPARTURE_DELAY >= 20"
QUERY_FLIGHTS_BY_ORIGIN = "SELECT flights.*, airlines.airline FROM flights JOIN airlines ON flights.airline = airlines.id WHERE flights.ORIGIN_AIRPORT = :origin"
QUERY_FLIGHTS_BY_DESTINATION = "SELECT flights.*, airlines.airline FROM flights JOIN airlines ON flights.airline = airlines.id WHERE flights.DESTINATION_AIRPORT = :destination"
QUERY_FLIGHTS_BY_DATE = "SELECT flights.*, airlines.airline FROM flights JOIN airlines ON flights.airline = airlines.id WHERE flights.DAY = :day AND flights.MONTH = :month AND flights.YEAR = :year"
QUERY_DELAYED_FLIGHTS_BY_AIRPORT = "SELECT flights.*, airlines.airline FROM flights JOIN airlines ON flights.airline = airlines.id WHERE flights.ORIGIN_AIRPORT = :origin AND flights.DEPARTURE_DELAY >= 20"
# Added missing queries for visualization functions
QUERY_DELAYED_FLIGHTS_BY_AIRLINE = "SELECT airlines.airline, COUNT(*) as delayed_flights FROM flights JOIN airlines ON flights.airline = airlines.id WHERE flights.DEPARTURE_DELAY >= 20 GROUP BY airlines.airline"
QUERY_TOTAL_FLIGHTS_BY_AIRLINE = "SELECT airlines.airline, COUNT(*) as total_flights FROM flights JOIN airlines ON flights.airline = airlines.id GROUP BY airlines.airline"
QUERY_DELAYED_FLIGHTS_BY_HOUR = "SELECT HOUR, COUNT(*) as delayed_flights FROM flights WHERE DEPARTURE_DELAY >= 20 GROUP BY HOUR ORDER BY HOUR"
QUERY_TOTAL_FLIGHTS_BY_HOUR = "SELECT HOUR, COUNT(*) as total_flights FROM flights GROUP BY HOUR ORDER BY HOUR"
QUERY_DELAYED_FLIGHTS_BY_ROUTE = "SELECT ORIGIN_AIRPORT, DESTINATION_AIRPORT, COUNT(*) as delayed_flights FROM flights WHERE DEPARTURE_DELAY >= 20 GROUP BY ORIGIN_AIRPORT, DESTINATION_AIRPORT"
QUERY_TOTAL_FLIGHTS_BY_ROUTE = "SELECT ORIGIN_AIRPORT, DESTINATION_AIRPORT, COUNT(*) as total_flights FROM flights GROUP BY ORIGIN_AIRPORT, DESTINATION_AIRPORT"


class FlightData:
    """
    The FlightData class is a Data Access Layer (DAL) object that provides an
    interface to the flight data in the SQLITE database. When the object is created,
    the class forms connection to the sqlite database file, which remains active
    until the object is destroyed.
    """

    def __init__(self, db_uri):
        """
        Initialize a new engine using the given database URI
        """
        self._engine = create_engine(db_uri)

    def _execute_query(self, query, params={}):
        """
        Execute an SQL query with the params provided in a dictionary,
        and returns a list of records (dictionary-like objects).
        If an exception was raised, print the error, and return an empty list.
        """
        try:
            with self._engine.connect() as connection:
                result = connection.execute(text(query), params)
                return [dict(row) for row in result]
        except Exception as e:
            print(f"Database query failed: {e}")
            return []

    def get_flight_by_id(self, flight_id):
        """
        Searches for flight details using flight ID.
        If the flight was found, returns a list with a single record.
        """
        params = {'id': flight_id}
        return self._execute_query(QUERY_FLIGHT_BY_ID, params)

    def get_delayed_flights(self):
        """
        Retrieves all flights that are delayed by 20 minutes or more.
        """
        return self._execute_query(QUERY_DELAYED_FLIGHTS)

    def get_flights_by_origin(self, origin):
        """
        Retrieves all flights departing from a specific origin airport.
        Ensures the origin is a valid 3-letter IATA code.
        """
        if not isinstance(origin, str) or len(origin) != 3 or not origin.isalpha():
            print("Invalid IATA code. Please enter a valid 3-letter airport code.")
            return []
        params = {'origin': origin.upper()}
        return self._execute_query(QUERY_FLIGHTS_BY_ORIGIN, params)

    def get_flights_by_destination(self, destination):
        """
        Retrieves all flights arriving at a specific destination airport.
        """
        params = {'destination': destination}
        return self._execute_query(QUERY_FLIGHTS_BY_DESTINATION, params)

    def get_flights_by_date(self, day, month, year):
        """
        Retrieves all flights scheduled on a specific date.
        """
        params = {'day': day, 'month': month, 'year': year}
        return self._execute_query(QUERY_FLIGHTS_BY_DATE, params)

    def get_delayed_flights_by_airport(self, origin):
        """
        Retrieves all flights from a specific origin airport that are delayed by 20+ minutes.
        Ensures the origin is a valid 3-letter IATA code.
        """
        if not isinstance(origin, str) or len(origin) != 3 or not origin.isalpha():
            print("Invalid IATA code. Please enter a valid 3-letter airport code.")
            return []
        params = {'origin': origin.upper()}
        return self._execute_query(QUERY_DELAYED_FLIGHTS_BY_AIRPORT, params)

    # Added missing methods for visualization
    def get_delayed_flights_by_airline(self, airline=None):
        """
        Retrieves count of delayed flights by airline.
        If airline is specified, filters by that airline name.
        """
        if airline:
            # Custom query for specific airline
            query = "SELECT airlines.airline, COUNT(*) as delayed_flights FROM flights JOIN airlines ON flights.airline = airlines.id WHERE airlines.airline = :airline AND flights.DEPARTURE_DELAY >= 20 GROUP BY airlines.airline"
            params = {'airline': airline}
            return self._execute_query(query, params)
        else:
            return self._execute_query(QUERY_DELAYED_FLIGHTS_BY_AIRLINE)

    def get_total_flights_by_airline(self):
        """
        Retrieves total count of flights by airline.
        """
        return self._execute_query(QUERY_TOTAL_FLIGHTS_BY_AIRLINE)

    def get_delayed_flights_by_hour(self):
        """
        Retrieves count of delayed flights by hour of day.
        """
        return self._execute_query(QUERY_DELAYED_FLIGHTS_BY_HOUR)

    def get_total_flights_by_hour(self):
        """
        Retrieves total count of flights by hour of day.
        """
        return self._execute_query(QUERY_TOTAL_FLIGHTS_BY_HOUR)

    def get_delayed_flights_by_route(self):
        """
        Retrieves count of delayed flights by route (origin-destination pair).
        """
        return self._execute_query(QUERY_DELAYED_FLIGHTS_BY_ROUTE)

    def get_total_flights_by_route(self):
        """
        Retrieves total count of flights by route (origin-destination pair).
        """
        return self._execute_query(QUERY_TOTAL_FLIGHTS_BY_ROUTE)

    def __del__(self):
        """
        Closes the connection to the database when the object is about to be destroyed
        """
        self._engine.dispose()