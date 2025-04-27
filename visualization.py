import matplotlib.pyplot as plt
import seaborn as sns
import folium
import pandas as pd
import webbrowser


def plot_delayed_flights_by_airline(data_manager):
    data = data_manager.get_delayed_flights_by_airline()
    if not data:
        print("No delayed flight data for airlines.")
        return

    df = pd.DataFrame(data)
    if df.empty:
        print("No delayed flight data for airlines (empty DataFrame).")
        return

    # 🔥 Fix: Rename 'airline_name' to 'airline' if needed
    if "airline_name" in df.columns and "airline" not in df.columns:
        df.rename(columns={"airline_name": "airline"}, inplace=True)

    if "airline" not in df.columns:
        print("Flight data still missing 'airline' column after renaming.")
        return

    plt.figure(figsize=(12, 6))
    sns.barplot(x="airline", y="delayed_flights", data=df)
    plt.title("Number of Delayed Flights per Airline")
    plt.xlabel("Airline")
    plt.ylabel("Number of Delayed Flights")
    plt.xticks(rotation=45)
    for index, row in df.iterrows():
        plt.text(index, row["delayed_flights"] + 2, int(row["delayed_flights"]), ha='center', va='bottom')
    plt.tight_layout()
    plt.show()


def plot_percentage_delayed_flights_by_airline(data_manager):
    delayed = data_manager.get_delayed_flights_by_airline()
    total = data_manager.get_total_flights_by_airline()

    if not delayed or not total:
        print("No data for percentage delayed flights per airline.")
        return

    delayed_df = pd.DataFrame(delayed)
    total_df = pd.DataFrame(total)

    if delayed_df.empty or total_df.empty:
        print("One of the datasets is empty.")
        return

    merged = pd.merge(delayed_df, total_df, on="airline")
    merged["percentage"] = (merged["delayed_flights"] / merged["total_flights"]) * 100

    plt.figure(figsize=(12, 6))
    sns.barplot(x="airline", y="percentage", data=merged)
    plt.title("Percentage of Delayed Flights per Airline")
    plt.xlabel("Airline")
    plt.ylabel("Percentage Delayed (%)")
    plt.xticks(rotation=45)
    for index, row in merged.iterrows():
        plt.text(index, row["percentage"] + 1, f"{row['percentage']:.1f}%", ha='center', va='bottom')
    plt.tight_layout()
    plt.show()


def plot_percentage_delayed_flights_by_hour(data_manager):
    delayed = data_manager.get_delayed_flights_by_hour()
    total = data_manager.get_total_flights_by_hour()

    if not delayed or not total:
        print("No data for delayed flights by hour.")
        return

    delayed_df = pd.DataFrame(delayed)
    total_df = pd.DataFrame(total)

    merged = pd.merge(delayed_df, total_df, on="hour")
    merged["percentage"] = (merged["delayed_flights"] / merged["total_flights"]) * 100
    merged = merged.sort_values("hour")

    plt.figure(figsize=(12, 6))
    sns.lineplot(x="hour", y="percentage", data=merged, marker="o")
    plt.title("Percentage of Delayed Flights by Hour")
    plt.xlabel("Hour of Day")
    plt.ylabel("Percentage Delayed (%)")
    plt.xticks(range(0, 24))
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_delays_heatmap_routes(data_manager):
    delayed_routes = data_manager.get_delayed_flights_by_route()

    if not delayed_routes:
        print("No delayed route data.")
        return

    df = pd.DataFrame(delayed_routes)
    if df.empty or "origin_airport" not in df.columns or "destination_airport" not in df.columns:
        print("Heatmap data missing necessary columns.")
        return

    pivot = df.pivot_table(index="origin_airport", columns="destination_airport", values="delayed_flights", fill_value=0)

    if pivot.empty:
        print("Heatmap has no data after pivot.")
        return

    plt.figure(figsize=(18, 14))
    sns.heatmap(pivot, cmap="YlOrRd", annot=True, fmt="d")
    plt.title("Heatmap of Delayed Flights by Route")
    plt.xlabel("Destination Airport")
    plt.ylabel("Origin Airport")
    plt.tight_layout()
    plt.show()


def plot_delays_on_map(data_manager):
    delayed_routes = data_manager.get_delayed_flights_by_route()

    if not delayed_routes:
        print("No delayed route data.")
        return

    df = pd.DataFrame(delayed_routes)
    if df.empty:
        print("No delayed route data (empty DataFrame).")
        return

    m = folium.Map(location=[20, 0], zoom_start=2)

    # Dummy example airport coordinates
    airport_coords = {
        "JFK": (40.6413, -73.7781),
        "LAX": (33.9416, -118.4085),
        "ORD": (41.9742, -87.9073),
        "SFO": (37.6213, -122.3790),
        "ATL": (33.6407, -84.4277),
        "SJU": (18.4394, -66.0018),
        "DFW": (32.8998, -97.0403),
        "DEN": (39.8561, -104.6737),
        "MIA": (25.7959, -80.2870),
    }

    for _, row in df.iterrows():
        origin = row.get("origin_airport")
        destination = row.get("destination_airport")
        count = row.get("delayed_flights")

        origin_coords = airport_coords.get(origin)
        destination_coords = airport_coords.get(destination)

        if origin_coords and destination_coords:
            folium.PolyLine(
                locations=[origin_coords, destination_coords],
                tooltip=f"{origin} ➔ {destination}: {count} delays",
                color="red",
                weight=2,
                opacity=0.7
            ).add_to(m)
        else:
            folium.Marker(
                location=[0, 0],
                popup=f"{origin} ➔ {destination}: {count} delays",
                icon=folium.Icon(color="red")
            ).add_to(m)

    m.save("delayed_routes_map.html")
    print("Map saved as 'delayed_routes_map.html'. Opening browser...")
    webbrowser.open("delayed_routes_map.html")