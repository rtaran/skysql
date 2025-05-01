from data import FlightData
from visualization import (
    plot_delayed_flights_by_airline,
    plot_percentage_delayed_flights_by_airline,
    plot_percentage_delayed_flights_by_hour,
    plot_delays_heatmap_routes,
    plot_delays_on_map,
    plot_percentage_delayed_routes_on_map,
)
import os

DB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "data", "flights.sqlite3")
)

# --- Helper Functions ---

def _print_table(data, fields):
    widths = [max(len(str(row.get(field, ""))) for row in data + [dict(zip(fields, fields))]) for field in fields]
    header = " ".join(field.ljust(width) for field, width in zip(fields, widths))
    separator = "-" * (sum(widths) + len(widths) - 1)

    print("\n=== Flight Information ===")
    print(header)
    print(separator)
    for row in data:
        print(" ".join(str(row.get(field, "")).ljust(width) for field, width in zip(fields, widths)))
    print(separator)


# --- Menu Actions ---

def show_flight_by_id(data_manager):
    flight_id = input("Enter flight ID: ").strip()
    if not flight_id.isdigit():
        print("Invalid ID. Please enter a number.")
        return

    flight = data_manager.get_flight_by_id(int(flight_id))
    if not flight:
        print("Flight not found.")
        return

    fields = ["id", "year", "month", "day", "origin_airport", "destination_airport", "delay"]
    _print_table(flight, fields)

def show_flights_by_date(data_manager):
    date_input = input("Enter date in DD/MM/YYYY format: ")
    try:
        day, month, year = map(int, date_input.split("/"))
    except ValueError:
        print("Invalid date format. Please use DD/MM/YYYY.")
        return

    flights = data_manager.get_flights_by_date(day, month, year)
    if not flights:
        print("No flights found on this date.")
        return

    fields = ["id", "year", "month", "day", "origin_airport", "destination_airport", "delay"]
    _print_table(flights, fields)

def delayed_flights_by_airline(data_manager):
    airline_name = input("Enter airline name (leave empty for all airlines): ").strip()

    data = data_manager.get_delayed_flights_by_airline(airline_name if airline_name else None)
    if not data:
        print("No delayed flights data found.")
        return

    print("\n=== Delayed Flights by Airline ===")
    for row in data:
        print(f"Airline: {row.get('airline', row.get('AIRLINE', 'Unknown'))}, Delayed Flights: {row.get('delayed_flights', row.get('DELAYED_FLIGHTS', 0))}")

def delayed_flights_by_origin(data_manager):
    """Show delayed flights by selected origin airport."""
    origin = input("Enter origin airport code: ").strip().upper()
    if len(origin) != 3 or not origin.isalpha():
        print("Invalid IATA code. Must be 3 alphabetic letters.")
        return

    data = data_manager.get_delayed_flights_by_airport(origin)
    if not data:
        print("No delayed flights found for this origin.")
        return

    print("\n=== Delayed Flights from Origin ===")
    for row in data:
        delay = row.get('delay', 'N/A')  # Safely get delay
        origin_airport = row.get('origin_airport', 'Unknown')
        destination_airport = row.get('destination_airport', 'Unknown')
        airline_name = row.get('airline_name', 'Unknown')
        print(f"Flight ID: {row.get('id', 'Unknown')}, Origin: {origin_airport}, Destination: {destination_airport}, Airline: {airline_name}, Delay: {delay} minutes")

def show_top_delayed_flights_by_date(data_manager):
    date_input = input("Enter date in DD/MM/YYYY format: ").strip()
    try:
        day, month, year = map(int, date_input.split("/"))
    except ValueError:
        print("Invalid date format. Please use DD/MM/YYYY.")
        return

    all_flights = data_manager.get_flights_by_date(day, month, year)
    if not all_flights:
        print("No flights found on this date.")
        return

    delayed_flights = data_manager.get_top_delayed_flights_by_date(day, month, year, 5)
    if not delayed_flights:
        print("Flights found, but no delayed flights on this date.")
        return

    fields = ["id", "flight_number", "origin", "delay"]
    _print_table(delayed_flights, fields)

def generate_visualizations(data_manager):
    print("\n=== Visualization Menu ===")
    print("1. Number of delayed flights by airline")
    print("2. Percentage of delayed flights by airline")
    print("3. Percentage of delayed flights by hour")
    print("4. Percentage of delayed flights per route on a Map (Origin <-> Destination, both directions average)")
    print("5. Heatmap of delayed flights by route")
    print("6. Delayed flights on a map")
    print("7. Generate all visualizations")
    print("8. Return to main menu")

    choice = input("\nSelect a visualization (1-8): ").strip()

    try:
        delayed_flights_data = data_manager.get_delayed_flights()
        if not delayed_flights_data:
            print("No delayed flight data available to visualize.")
            return

        if choice == "1":
            plot_delayed_flights_by_airline(data_manager)
        elif choice == "2":
            plot_percentage_delayed_flights_by_airline(data_manager)
        elif choice == "3":
            plot_percentage_delayed_flights_by_hour(data_manager)
        elif choice == "4":
            plot_percentage_delayed_routes_on_map(data_manager)
        elif choice == "5":
            plot_delays_heatmap_routes(data_manager)
        elif choice == "6":
            plot_delays_on_map(data_manager)
        elif choice == "7":
            plot_delayed_flights_by_airline(data_manager)
            plot_percentage_delayed_flights_by_airline(data_manager)
            plot_percentage_delayed_flights_by_hour(data_manager)
            plot_percentage_delayed_routes_on_map(data_manager)
            plot_delays_heatmap_routes(data_manager)
            plot_delays_on_map(data_manager)
        elif choice == "8":
            return
        else:
            print("Invalid choice. Please select a number between 1 and 8.")
    except Exception as e:
        print(f"Visualization failed: {e}")

def quit_program(data_manager):
    print("Exiting program. Goodbye!")
    quit()

# --- Main Loop ---

def main():
    print(f"Using database at: {DB_PATH}")
    data_manager = FlightData(f"sqlite:///{DB_PATH}")

    menu_options = {
        "1": show_flight_by_id,
        "2": show_flights_by_date,
        "3": delayed_flights_by_airline,
        "4": delayed_flights_by_origin,
        "5": show_top_delayed_flights_by_date,
        "6": generate_visualizations,
        "7": quit_program,
    }

    while True:
        print("\n" + "=" * 40)
        print(" FLIGHT DATA QUERY MENU ".center(40, "-"))
        print("=" * 40)
        print("1. Show flight by ID")
        print("2. Show flights by date")
        print("3. Delayed flights by airline")
        print("4. Delayed flights by origin airport")
        print("5. Top 5 delayed flights by date")
        print("6. Generate visualizations")
        print("7. Exit")
        print("=" * 40)

        choice = input("Select an option: ").strip()
        choice_func = menu_options.get(choice)

        if not choice_func:
            print("\n❗ Invalid option, please select a number between 1 and 7.\n")
            continue

        choice_func(data_manager)
        input("\nPress Enter to return to Main Menu...")

if __name__ == "__main__":
    main()
