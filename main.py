from data import FlightData
from visualization import (
    plot_delayed_flights_by_airline,
    plot_percentage_delayed_flights_by_airline,
    plot_percentage_delayed_flights_by_hour,
    plot_delays_heatmap_routes,
    plot_delays_on_map,
)
import os


DB_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "data", "flights.sqlite3")
)


def show_flight_by_id(data_manager):
    flight_id = input("Enter flight ID: ")
    flight = data_manager.get_flight_by_id(flight_id)
    if flight:
        print(flight)
    else:
        print("Flight not found.")


def show_flights_by_date(data_manager):
    date_input = input("Enter date in DD/MM/YYYY format: ")
    try:
        day, month, year = date_input.split("/")
    except ValueError:
        print("Invalid date format. Please use DD/MM/YYYY.")
        return
    flights = data_manager.get_flights_by_date(day, month, year)
    if flights:
        for f in flights:
            print(f)
    else:
        print("No flights found on this date.")


def show_top_delayed_flights_by_date(data_manager):
    date_input = input("Enter date in DD/MM/YYYY format: ")
    try:
        day, month, year = date_input.split("/")
    except ValueError:
        print("Invalid date format. Please use DD/MM/YYYY.")
        return
    flights = data_manager.get_top_delayed_flights_by_date(day, month, year, 5)
    if flights:
        for f in flights:
            print(f)
    else:
        print("No delayed flights found on this date.")


def delayed_flights_by_airline(data_manager):
    data = data_manager.get_delayed_flights_by_airline()
    for row in data:
        print(f"Airline: {row['airline']}, Delayed Flights: {row['delayed_flights']}")


def delayed_flights_by_origin(data_manager):
    origin = input("Enter origin airport code: ")
    data = data_manager.get_delayed_flights_by_airport(origin)
    if data:
        for row in data:
            print(f"Flight ID: {row['id']}, Delay: {row['delay']}")
    else:
        print("No delayed flights found for this origin.")


def quit_program(data_manager):
    print("Exiting program.")
    quit()


def main():
    print(f"Using database at: {DB_PATH}")
    data_manager = FlightData(f"sqlite:///{DB_PATH}")

    menu_options = {
        "1": show_flight_by_id,
        "2": show_flights_by_date,
        "3": delayed_flights_by_airline,
        "4": delayed_flights_by_origin,
        "5": show_top_delayed_flights_by_date,
        "6": quit_program,
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
        print("6. Exit")
        print("=" * 40)

        choice = input("Select an option: ").strip()

        choice_func = menu_options.get(choice)
        if not choice_func:
            print("Invalid option, please try again.")
            continue

        choice_func(data_manager)

        # After executing the chosen function, plot visualizations
        try:
            print("Attempting to generate visualizations...")
            if hasattr(data_manager, "get_delayed_flights"):
                delayed_flights_data = data_manager.get_delayed_flights()
                if delayed_flights_data:
                    plot_delayed_flights_by_airline(data_manager)
                    plot_percentage_delayed_flights_by_airline(data_manager)
                    plot_percentage_delayed_flights_by_hour(data_manager)
                    plot_delays_heatmap_routes(data_manager)
                    plot_delays_on_map(data_manager)
                else:
                    print("No delayed flight data available to visualize.")
            else:
                print("Data manager does not support delayed flights retrieval. Skipping visualization.")
        except Exception as e:
            print(f"Visualization failed: {e}")


if __name__ == "__main__":
    main()