from sqlalchemy import create_engine, text
import matplotlib.pyplot as plt

class FlightData:
    def __init__(self, uri):
        self.engine = create_engine(uri)

    def get_flight_by_id(self, flight_id):
        with self.engine.connect() as conn:
            result = conn.execute(
                text("SELECT * FROM flights WHERE id = :id"),
                parameters={"id": flight_id}
            ).fetchall()
            return [dict(row._mapping) for row in result]

    def get_flights_by_date(self, day, month, year):
        with self.engine.connect() as conn:
            result = conn.execute(
                text(
                    "SELECT * FROM flights WHERE day = :day AND month = :month AND year = :year"
                ),
                parameters={"day": day, "month": month, "year": year}
            ).fetchall()
            return [dict(row._mapping) for row in result]

    def get_delayed_flights_by_airline(self, airline=None):
        if airline:
            query = """
            SELECT airlines.airline AS airline, COUNT(*) as delayed_flights
            FROM flights
            JOIN airlines ON flights.airline = airlines.id
            WHERE airlines.airline = :airline AND flights.departure_delay >= 20
            GROUP BY airlines.airline
            """
            params = {"airline": airline}
            with self.engine.connect() as conn:
                result = conn.execute(text(query), parameters=params).fetchall()
            return [dict(row._mapping) for row in result]
        else:
            query = """
            SELECT airlines.airline AS airline, COUNT(*) as delayed_flights
            FROM flights
            JOIN airlines ON flights.airline = airlines.id
            WHERE flights.departure_delay >= 20
            GROUP BY airlines.airline
            """
            with self.engine.connect() as conn:
                result = conn.execute(text(query)).fetchall()
            return [dict(row._mapping) for row in result]

    def get_total_flights_by_airline(self):
        with self.engine.connect() as conn:
            result = conn.execute(
                text(
                    "SELECT airline, COUNT(*) as total_flights FROM flights GROUP BY airline"
                )
            ).fetchall()
            return [dict(row._mapping) for row in result]

    def get_delayed_flights_by_airport(self, airport_code):
        with self.engine.connect() as conn:
            result = conn.execute(
                text(
                    "SELECT * FROM flights WHERE origin_airport = :airport AND departure_delay > 0"
                ),
                parameters={"airport": airport_code}
            ).fetchall()
            return [dict(row._mapping) for row in result]

    def get_delayed_flights_by_hour(self):
        with self.engine.connect() as conn:
            result = conn.execute(
                text(
                    "SELECT strftime('%H', scheduled_departure) AS hour, COUNT(*) as delayed_flights FROM flights WHERE departure_delay > 0 GROUP BY hour ORDER BY hour"
                )
            ).fetchall()
            return [dict(row._mapping) for row in result]

    def get_total_flights_by_hour(self):
        with self.engine.connect() as conn:
            result = conn.execute(
                text(
                    "SELECT hour, COUNT(*) as total_flights FROM flights GROUP BY hour"
                )
            ).fetchall()
            return [dict(row._mapping) for row in result]

def plot_delayed_flights_by_airline(data_manager):
    """
    Plots the number of delayed flights by airline.
    """
    stats = data_manager.get_delayed_flights_by_airline()
    if not stats:
        print("No delayed flight data to plot.")
        return

    stats = sorted(stats, key=lambda x: x["delayed_flights"], reverse=True)

    airlines = [row["airline"] for row in stats]
    delays = [row["delayed_flights"] for row in stats]

    plt.figure(figsize=(12, 7))
    plt.bar(airlines, delays, color="skyblue")
    plt.xlabel("Airline")
    plt.ylabel("Number of Delayed Flights")
    plt.title("Delayed Flights by Airline")
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def plot_delayed_flights_by_hour(data_manager):
    stats = data_manager.get_delayed_flights_by_hour()
    if not stats:
        print("No delayed flight data to plot.")
        return

    stats = sorted(stats, key=lambda x: int(x["hour"]))

    hours = [int(row["hour"]) for row in stats]
    delays = [row["delayed_flights"] for row in stats]

    plt.figure(figsize=(12, 7))
    plt.bar(hours, delays, color="orange")
    plt.xlabel("Hour of Day")
    plt.ylabel("Number of Delayed Flights")
    plt.title("Delayed Flights by Hour")
    plt.xticks(hours)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def plot_percentage_delayed_flights_by_airline(data_manager):
    delayed_stats = data_manager.get_delayed_flights_by_airline()
    total_stats = data_manager.get_total_flights_by_airline()

    total_lookup = {row["airline"]: row["total_flights"] for row in total_stats}
    stats = []
    for row in delayed_stats:
        airline = row["airline"]
        delayed = row["delayed_flights"]
        total = total_lookup.get(airline, 1)
        stats.append({
            "airline": airline,
            "percentage": (delayed / total) * 100
        })

    stats = sorted(stats, key=lambda x: x["percentage"], reverse=True)
    airlines = [row["airline"] for row in stats]
    percentages = [row["percentage"] for row in stats]

    plt.figure(figsize=(12, 7))
    plt.bar(airlines, percentages, color="skyblue")
    plt.xlabel("Airline")
    plt.ylabel("Percentage of Delayed Flights (%)")
    plt.title("Percentage of Delayed Flights by Airline")
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def plot_percentage_delayed_flights_by_hour(data_manager):
    delayed_stats = data_manager.get_delayed_flights_by_hour()
    total_stats = data_manager.get_total_flights_by_hour()

    total_lookup = {row["hour"]: row["total_flights"] for row in total_stats}
    stats = []
    for row in delayed_stats:
        hour = row["hour"]
        delayed = row["delayed_flights"]
        total = total_lookup.get(hour, 1)
        stats.append({
            "hour": hour,
            "percentage": (delayed / total) * 100
        })

    stats = sorted(stats, key=lambda x: int(x["hour"]))
    hours = [int(row["hour"]) for row in stats]
    percentages = [row["percentage"] for row in stats]

    plt.figure(figsize=(12, 7))
    plt.bar(hours, percentages, color="orange")
    plt.xlabel("Hour of Day")
    plt.ylabel("Percentage of Delayed Flights (%)")
    plt.title("Percentage of Delayed Flights by Hour")
    plt.xticks(hours)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

def plot_delays_heatmap_routes(data_manager):
    print("Heatmap of routes - placeholder function. To be implemented with seaborn or similar.")

def plot_delays_on_map(data_manager):
    print("Map of routes - placeholder function. To be implemented with folium or similar.")