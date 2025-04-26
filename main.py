from visualization import FlightData, plot_delayed_flights_by_airline, plot_delayed_flights_by_hour, plot_percentage_delayed_flights_by_airline, plot_percentage_delayed_flights_by_hour, plot_delays_heatmap_routes, plot_delays_on_map
import os
import sqlite3

DB_PATH = os.path.join("data", "flights.sqlite3")


class DataManager:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

    def get_flight_by_id(self, flight_id):
        cursor = self.conn.execute("SELECT * FROM flights WHERE id = ?", (flight_id,))
        return cursor.fetchone()

    def get_flights_by_date(self, date):
        cursor = self.conn.execute("SELECT * FROM flights WHERE date = ?", (date,))
        return cursor.fetchall()

    def get_delayed_flights_by_airline(self):
        cursor = self.conn.execute(
            "SELECT airline, COUNT(*) as delay_count FROM flights WHERE delay > 0 GROUP BY airline"
        )
        return cursor.fetchall()

    def get_delayed_flights_by_origin(self):
        cursor = self.conn.execute(
            "SELECT origin, COUNT(*) as delay_count FROM flights WHERE delay > 0 GROUP BY origin"
        )
        return cursor.fetchall()


def show_flight_by_id(data_manager):
    flight_id = input("Enter flight ID: ")
    flight = data_manager.get_flight_by_id(flight_id)
    if flight:
        print(dict(flight))
    else:
        print("Flight not found.")


def show_flights_by_date(data_manager):
    date = input("Enter date (YYYY-MM-DD): ")
    flights = data_manager.get_flights_by_date(date)
    if flights:
        for flight in flights:
            print(dict(flight))
    else:
        print("No flights found on this date.")


def delayed_flights_by_airline(data_manager):
    data = data_manager.get_delayed_flights_by_airline()
    for row in data:
        print(f"Airline: {row['airline']}, Delayed Flights: {row['delay_count']}")


def delayed_flights_by_origin(data_manager):
    data = data_manager.get_delayed_flights_by_origin()
    for row in data:
        print(f"Origin: {row['origin']}, Delayed Flights: {row['delay_count']}")


def quit_program(data_manager):
    print("Exiting program.")


def main():
    print(f"Using database at: {os.path.abspath(DB_PATH)}")
    data_manager = FlightData(f"sqlite:///{DB_PATH}")

    menu_options = {
        "1": show_flight_by_id,
        "2": show_flights_by_date,
        "3": delayed_flights_by_airline,
        "4": delayed_flights_by_origin,
        "5": quit_program,
    }

    while True:
        print("Menu:")
        print("1. Show flight by ID")
        print("2. Show flights by date")
        print("3. Delayed flights by airline")
        print("4. Delayed flights by origin airport")
        print("5. Exit")

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

        try:
            plot_percentage_delayed_flights_by_airline(data_manager)
            plot_percentage_delayed_flights_by_hour(data_manager)
            plot_delays_heatmap_routes(data_manager)
            plot_delays_on_map(data_manager)
        except Exception as e:
            print(f"Visualization failed: {e}")

        choice = input("Select an option: ").strip()

        choice_func = menu_options.get(choice)
        if not choice_func:
            print("Invalid option, please try again.")
            continue

        if choice_func == quit_program:
            quit()
        else:
            choice_func(data_manager)


if __name__ == "__main__":
    main()