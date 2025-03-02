# Flight Data API

A comprehensive platform for accessing and visualizing flight delay data. This project includes both a command-line interface and a RESTful API for querying flight information.

## Features

- **Command-line Interface**: Query flight data interactively
- **RESTful API**: Access flight data through HTTP requests
- **Data Visualization**: Generate charts and graphs showing flight delay patterns
- **Comprehensive Querying**: Search by flight ID, date, airline, airport, and more
- **Statistical Analysis**: Analyze delay patterns across airlines, times, and routes

## Project Structure

```
flight-data-api/
├── data.py              # Data access layer (SQLite database connector)
├── main.py              # Command-line interface application
├── api.py               # Flask REST API
├── visualization.py     # Data visualization utilities
├── requirements.txt     # Project dependencies
├── LICENSE              # MIT License file
├── .gitignore           # Git ignore file
├── flights.sqlite3      # SQLite database with flight data (not included in repo)
└── README.md            # This file
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/flight-data-api.git
cd flight-data-api
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Place your `flights.sqlite3` database file in the project root directory.

## Usage

### Command-line Interface

Run the command-line interface:
```bash
python main.py
```

This will present a menu where you can:
1. Query flight information by ID
2. View flights by date
3. Check delayed flights by airline
4. Find delayed flights by origin airport
5. Exit the application

The application will also attempt to generate visualizations of flight delay data.

### REST API

Start the API server:
```bash
python api.py
```

The API will be available at `http://localhost:5000/`. Some example endpoints:

- `GET /api/flights/{flight_id}` - Get flight details by ID
- `GET /api/flights/date/{year}/{month}/{day}` - Get flights by date
- `GET /api/flights/delayed` - Get all delayed flights
- `GET /api/flights/origin/{origin_code}` - Get flights by origin airport
- `GET /api/stats/airlines` - Get airline delay statistics

See the API documentation for a full list of endpoints.

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