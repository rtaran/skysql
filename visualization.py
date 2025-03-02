import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def plot_delayed_flights_by_airline(flight_data):
    """
    Creates a bar chart showing the percentage of delayed flights by airline.
    """
    # Get data - error handling in case results are empty
    delayed_data = flight_data.get_delayed_flights_by_airline()
    total_data = flight_data.get_total_flights_by_airline()

    if not delayed_data or not total_data:
        print("No data available to visualize")
        return

    delayed = pd.DataFrame(delayed_data)
    total = pd.DataFrame(total_data)

    # Make sure we have data to merge
    if delayed.empty or total.empty:
        print("Insufficient data to create visualization")
        return

    # Create merged dataframe with percentage calculation
    merged = pd.merge(delayed, total, on='airline')
    merged['percentage_delayed'] = (merged['delayed_flights'] / merged['total_flights']) * 100

    # Create visualization
    plt.figure(figsize=(12, 6))
    sns.barplot(x='airline', y='percentage_delayed', data=merged, color='blue')
    plt.xticks(rotation=45, ha='right')
    plt.xlabel('Airline')
    plt.ylabel('Percentage of Delayed Flights')
    plt.title('Percentage of Delayed Flights by Airline')
    plt.tight_layout()  # Added to prevent labels from being cut off
    plt.show()


def plot_delayed_flights_by_hour(flight_data):
    """
    Creates a bar chart showing the percentage of delayed flights by hour of the day.
    """
    # Get data with error handling
    delayed_data = flight_data.get_delayed_flights_by_hour()
    total_data = flight_data.get_total_flights_by_hour()

    if not delayed_data or not total_data:
        print("No data available to visualize")
        return

    delayed = pd.DataFrame(delayed_data)
    total = pd.DataFrame(total_data)

    # Make sure we have data to merge
    if delayed.empty or total.empty:
        print("Insufficient data to create visualization")
        return

    # Create merged dataframe with percentage calculation
    merged = pd.merge(delayed, total, on='hour')
    merged['percentage_delayed'] = (merged['delayed_flights'] / merged['total_flights']) * 100

    # Create visualization
    plt.figure(figsize=(12, 6))
    sns.barplot(x='hour', y='percentage_delayed', data=merged, palette='viridis')
    plt.xlabel('Hour of Day')
    plt.ylabel('Percentage of Delayed Flights')
    plt.title('Percentage of Delayed Flights by Hour of Day')
    plt.tight_layout()
    plt.show()


def plot_delayed_flights_by_route(flight_data):
    """
    Creates a heatmap showing the percentage of delayed flights by route.
    This function assumes data contains origin and destination airports.
    """
    # Get data with error handling
    delayed_data = flight_data.get_delayed_flights_by_route()
    total_data = flight_data.get_total_flights_by_route()

    if not delayed_data or not total_data:
        print("No data available to visualize")
        return

    delayed = pd.DataFrame(delayed_data)
    total = pd.DataFrame(total_data)

    # Make sure we have data to merge and it contains required columns
    if (delayed.empty or total.empty or
            'ORIGIN_AIRPORT' not in delayed.columns or
            'DESTINATION_AIRPORT' not in delayed.columns):
        print("Insufficient data to create visualization")
        return

    # Create merged dataframe with percentage calculation
    try:
        merged = pd.merge(delayed, total, on=['ORIGIN_AIRPORT', 'DESTINATION_AIRPORT'])
        merged['percentage_delayed'] = (merged['delayed_flights'] / merged['total_flights']) * 100

        # Create pivot table for heatmap (with error handling for empty data)
        if len(merged) > 0:
            pivot_table = merged.pivot_table(
                values='percentage_delayed',
                index='ORIGIN_AIRPORT',
                columns='DESTINATION_AIRPORT',
                fill_value=0
            )

            # Create visualization
            plt.figure(figsize=(12, 10))
            sns.heatmap(pivot_table, cmap='Reds', linewidths=0.5)
            plt.xlabel('Destination Airport')
            plt.ylabel('Origin Airport')
            plt.title('Percentage of Delayed Flights by Route')
            plt.tight_layout()
            plt.show()
        else:
            print("Not enough routes to create heatmap")
    except Exception as e:
        print(f"Error creating route visualization: {e}")


def plot_routes_on_map(flight_data):
    """
    Creates a map visualization of flight routes with delay information.
    Note: This function requires geopandas and Basemap which might need
    to be installed separately.
    """
    try:
        import geopandas as gpd
        from mpl_toolkits.basemap import Basemap
    except ImportError:
        print("Required libraries for map visualization not installed.")
        print("Please install geopandas and basemap with:")
        print("pip install geopandas mpl_toolkits.basemap")
        return

    # Get data with error handling
    delayed_data = flight_data.get_delayed_flights_by_route()
    total_data = flight_data.get_total_flights_by_route()

    if not delayed_data or not total_data:
        print("No data available to visualize")
        return

    try:
        delayed = pd.DataFrame(delayed_data)
        total = pd.DataFrame(total_data)

        # This function requires additional location data that might not be present
        # We'd need airport coordinates to be in the dataset
        required_columns = ['ORIGIN_AIRPORT', 'DESTINATION_AIRPORT',
                            'ORIGIN_AIRPORT_LAT', 'ORIGIN_AIRPORT_LON',
                            'DESTINATION_AIRPORT_LAT', 'DESTINATION_AIRPORT_LON']

        # Check if we have all required location data
        if not all(col in delayed.columns for col in required_columns):
            print("Required location data missing from dataset.")
            print("This visualization needs airport latitude and longitude data.")
            return

        merged = pd.merge(delayed, total, on=['ORIGIN_AIRPORT', 'DESTINATION_AIRPORT'])
        merged['percentage_delayed'] = (merged['delayed_flights'] / merged['total_flights']) * 100

        plt.figure(figsize=(12, 8))
        m = Basemap(projection='merc', llcrnrlat=20, urcrnrlat=55,
                    llcrnrlon=-130, urcrnrlon=-60, resolution='l')
        m.drawcoastlines()
        m.drawcountries()
        m.drawstates()

        for _, row in merged.iterrows():
            origin_x, origin_y = m(row['ORIGIN_AIRPORT_LON'], row['ORIGIN_AIRPORT_LAT'])
            dest_x, dest_y = m(row['DESTINATION_AIRPORT_LON'], row['DESTINATION_AIRPORT_LAT'])
            color = 'red' if row['percentage_delayed'] > 50 else 'green'
            plt.plot([origin_x, dest_x], [origin_y, dest_y], color=color, linewidth=2)

        plt.title('Percentage of Delayed Flights Per Route')
        plt.show()
    except Exception as e:
        print(f"Error creating map visualization: {e}")