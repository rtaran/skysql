import os
from data import FlightData
from datetime import datetime
import sqlalchemy
from visualization import plot_delayed_flights_by_airline, plot_delayed_flights_by_hour

# Constants
IATA_LENGTH = 3  # Standard IATA airport code length

# Get the absolute path to the database file
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, "flights.sqlite3")
SQLITE_URI = f"sqlite:///{db_path}"

print(f"Using database at: {db_path}")
if not os.path.exists(db_path):
    print(f"WARNING: Database file not found at {db_path}")


def delayed_flights_by_airline(data_manager):
    """
    Asks the user for a textual airline name (any string will work here).
    Then runs the query using the data object method "get_delayed_flights_by_airline".
    When results are back, calls "print_results" to show them to on the screen.
    """
    airline_input = input("Enter airline name: ")
    results = data_manager.get_delayed_flights_by_airline(airline_input)
    print_results(results)


def delayed_flights_by_airport(data_manager):
    """
    Asks the user for a textual IATA 3-letter airport code (loops until input is valid).
    Then runs the query using the data object method "get_delayed_flights_by_airport".
    When results are back, calls "print_results" to show them to on the screen.
    """
    valid = False
    while not valid:
        airport_input = input("Enter origin airport IATA code: ")
        # Validate input
        if airport_input.isalpha() and len(airport_input) == IATA_LENGTH:
            valid = True
    results = data_manager.get_delayed_flights_by_airport(airport_input)
    print_results(results)


def flight_by_id(data_manager):
    """
    Asks the user for a numeric flight ID,
    Then runs the query using the data object method "get_flight_by_id".
    When results are back, calls "print_results" to show them to on the screen.
    """
    valid = False
    while not valid:
        try:
            id_input = int(input("Enter flight ID: "))
        except Exception as e:
            print("Try again...")
        else:
            valid = True
    results = data_manager.get_flight_by_id(id_input)
    print_results(results)


def flights_by_date(data_manager):
    """
    Asks the user for date input (and loops until it's valid),
    Then runs the query using the data object method "get_flights_by_date".
    When results are back, calls "print_results" to show them to on the screen.
    """
    valid = False
    while not valid:
        try:
            date_input = input("Enter date in DD/MM/YYYY format: ")
            date = datetime.strptime(date_input, '%d/%m/%Y')
        except ValueError as e:
            print("Try again...", e)
        else:
            valid = True
    results = data_manager.get_flights_by_date(date.day, date.month, date.year)
    print_results(results)


def print_results(results):
    """
    Get a list of flight results (List of dictionary objects from data layer).
    Even if there is one result, it should be provided in a list.
    Each object *has* to contain the columns:
    ID, ORIGIN_AIRPORT, DESTINATION_AIRPORT, AIRLINE, and DELAY.
    """
    print(f"Got {len(results)} results.")
    for result in results:
        # Check that all required columns are in place
        try:
            # Results are already dictionaries, no need for _mapping
            delay = int(result.get('DELAY', 0)) if result.get('DELAY') else 0
            origin = result.get('ORIGIN_AIRPORT', 'N/A')
            dest = result.get('DESTINATION_AIRPORT', 'N/A')
            airline = result.get('AIRLINE', 'N/A')
            flight_id = result.get('ID', result.get('FLIGHT_ID', 'N/A'))
        except (ValueError, sqlalchemy.exc.SQLAlchemyError) as e:
            print("Error showing results: ", e)
            continue

        # Different prints for delayed and non-delayed flights
        if delay and delay > 0:
            print(f"{flight_id}. {origin} -> {dest} by {airline}, Delay: {delay} Minutes")
        else:
            print(f"{flight_id}. {origin} -> {dest} by {airline}")


def show_menu_and_get_input():
    """
    Show the menu and get user input.
    If it's a valid option, return a pointer to the function to execute.
    Otherwise, keep asking the user for input.
    """
    print("Menu:")
    for key, value in FUNCTIONS.items():
        print(f"{key}. {value[1]}")

    # Input loop
    while True:
        try:
            choice = int(input())
            if choice in FUNCTIONS:
                return FUNCTIONS[choice][0]
        except ValueError as e:
            pass
        print("Try again...")


"""
Function Dispatch Dictionary
"""
FUNCTIONS = {1: (flight_by_id, "Show flight by ID"),
             2: (flights_by_date, "Show flights by date"),
             3: (delayed_flights_by_airline, "Delayed flights by airline"),
             4: (delayed_flights_by_airport, "Delayed flights by origin airport"),
             5: (quit, "Exit")
             }


def main():
    # Create an instance of the Data Object using our SQLite URI
    data_manager = FlightData(SQLITE_URI)

    # Try different visualizations - only enable the ones that work
    try:
        print("Attempting to generate airline delay visualization...")
        plot_delayed_flights_by_airline(data_manager)
    except Exception as e:
        print(f"Visualization failed: {e}")

    try:
        print("Attempting to generate hourly delay visualization...")
        plot_delayed_flights_by_hour(data_manager)
    except Exception as e:
        print(f"Visualization failed: {e}")

    # The Main Menu loop
    while True:
        choice_func = show_menu_and_get_input()
        choice_func(data_manager)


if __name__ == "__main__":
    main()