# Sky SQL - Flight Data Analysis Platform

A comprehensive platform for accessing, analyzing, and visualizing flight delay data. This project includes both a command-line interface and a RESTful API for querying flight information, as well as powerful visualization tools to help identify patterns in flight delays.

## Features

- **Command-line Interface**: Query flight data interactively
- **RESTful API**: Access flight data through HTTP requests
- **Data Visualization**: Generate charts, graphs, and maps showing flight delay patterns:
  - Bar charts of delayed flights by airline
  - Percentage analysis of delays by airline and hour
  - Interactive maps showing delayed routes
  - Heatmaps of delay patterns
  - Route maps with color-coded delay percentages
- **Comprehensive Querying**: Search by flight ID, date, airline, airport, and more
- **Statistical Analysis**: Analyze delay patterns across airlines, times, and routes
- **Interactive Visualization Menu**: Choose from multiple visualization options

## Project Structure

```
sky-sql/
├── data/
│   └── flights.sqlite3  # SQLite database with flight data
├── tests/
│   ├── test_api.py      # API tests
│   └── test_data.py     # Data layer tests
├── data.py              # Data access layer (SQLite database connector)
├── main.py              # Command-line interface application
├── api.py               # Flask REST API
├── visualization.py     # Data visualization utilities
├── requirements.txt     # Project dependencies
├── setup.py             # Package setup file
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose configuration
├── license              # License file
├── CONTRIBUTING.md      # Contributing guidelines
└── README.md            # This file
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/sky-sql.git
cd sky-sql
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Ensure the `flights.sqlite3` database file is in the `data/` directory. If not, create the directory and place the file there:
```bash
mkdir -p data
# Copy your flights.sqlite3 file to the data directory
```

4. Alternatively, you can use Docker to run the application:
```bash
docker-compose up
```

## Usage

### Command-line Interface

Run the command-line interface:
```bash
python main.py
```

This will present a menu where you can:
1. Show flight by ID
2. Show flights by date
3. Delayed flights by airline
4. Delayed flights by origin airport
5. Top 5 delayed flights by date
6. Generate visualizations
7. Exit

The visualization menu offers several options:
1. Number of delayed flights by airline
2. Percentage of delayed flights by airline
3. Percentage of delayed flights by hour
4. Percentage of delayed flights per route on a Map (Origin <-> Destination, both directions average)
5. Heatmap of delayed flights by route
6. Delayed flights on a map
7. Generate all visualizations

### REST API

Start the API server:
```bash
python api.py
```

The API will be available at `http://localhost:5000/`. Available endpoints:

- `GET /` - API information and available endpoints
- `GET /api/flights/{flight_id}` - Get flight details by ID
- `GET /api/flights/date/{year}/{month}/{day}` - Get flights by date
- `GET /api/flights/delayed` - Get all delayed flights
- `GET /api/flights/origin/{origin_code}` - Get flights by origin airport
- `GET /api/flights/destination/{destination_code}` - Get flights by destination airport
- `GET /api/flights/delayed/origin/{origin_code}` - Get delayed flights by origin airport
- `GET /api/flights/delayed/airline/{airline_name}` - Get delayed flights by airline
- `GET /api/stats/airlines` - Get airline delay statistics
- `GET /api/stats/hours` - Get hourly delay statistics
- `GET /api/stats/routes` - Get route delay statistics

All API responses are in JSON format and include a `success` flag and either a `data` array or an `error` message.

## Database Schema

The database contains the following main tables:
- `flights`: Contains flight records with delay information
- `airlines`: Contains airline information

Key columns in the flights table include:
- `ID`: Unique flight identifier
- `ORIGIN_AIRPORT`: 3-letter IATA code for origin airport
- `DESTINATION_AIRPORT`: 3-letter IATA code for destination airport
- `DEPARTURE_DELAY`: Delay in minutes
- `DAY`, `MONTH`, `YEAR`: Flight date
- `HOUR`: Hour of scheduled departure

## Requirements

- Python 3.7 or higher
- Flask 2.0 or higher
- SQLAlchemy 1.4 or higher
- Matplotlib 3.5 or higher
- Seaborn 0.11 or higher
- Pandas 1.3 or higher
- Folium (for interactive maps)
- Webbrowser (standard library, for opening maps)

The application can also be run using Docker with the provided Dockerfile and docker-compose.yml.

See `requirements.txt` for a complete list of dependencies.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
