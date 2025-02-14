import os
import pyodbc
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_CONNECTION_STRING = os.getenv('DB_CONNECTION_STRING')
API_KEY = os.getenv('API_KEY')

if not DB_CONNECTION_STRING:
    raise ValueError("DB_CONNECTION_STRING environment variable is not set.")
if not API_KEY:
    raise ValueError("API_KEY environment variable is not set.")

print("Starting script...")

def fetch_weather_data(city, date):
    """Fetch weather data from OpenWeatherMap API."""
    try:
        print(f"Fetching weather data for {city} on {date}...")
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&dt={date}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        print(f"Response status code: {response.status_code}")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {city} on {date}: {e}")
        return None

def create_table():
    """Create the weather_data table if it doesn't exist."""
    try:
        print("Connecting to the database...")
        conn = pyodbc.connect(DB_CONNECTION_STRING)
        cursor = conn.cursor()
        print("Creating table...")
        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='weather_data' AND xtype='U')
            CREATE TABLE weather_data (
                id INTEGER PRIMARY KEY IDENTITY(1,1),
                city NVARCHAR(100),
                date TEXT,
                temperature FLOAT,
                humidity FLOAT,
                pressure FLOAT
            )
        ''')
        conn.commit()
        conn.close()
        print("Table created or already exists.")
    except pyodbc.Error as e:
        print(f"Error creating table: {e}")
    """Create the weather_data table if it doesn't exist."""
    try:
        print("Connecting to the database...")
        conn = pyodbc.connect(DB_CONNECTION_STRING)
        cursor = conn.cursor()
        print("Creating table...")
        cursor.execute('''
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='weather_data' AND xtype='U')
            CREATE TABLE weather_data (
                id INTEGER PRIMARY KEY IDENTITY(1,1),
                city TEXT,
                date TEXT,
                temperature FLOAT,
                humidity FLOAT,
                pressure FLOAT
            )
        ''')
        conn.commit()
        conn.close()
        print("Table created or already exists.")
    except pyodbc.Error as e:
        print(f"Error creating table: {e}")

def insert_weather_data(city, date, temperature, humidity, pressure):
    """Insert weather data into the database."""
    try:
        # Convert temperature from Kelvin to Celsius
        temperature_celsius = temperature - 273.15
        print(f"Inserting data for {city} on {date}...")
        conn = pyodbc.connect(DB_CONNECTION_STRING)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO weather_data (city, date, temperature, humidity, pressure)
            VALUES (?, ?, ?, ?, ?)
        ''', (city, date, temperature_celsius, humidity, pressure))
        conn.commit()
        conn.close()
        print("Data inserted successfully.")
    except pyodbc.Error as e:
        print(f"Error inserting data: {e}")
    """Insert weather data into the database."""
    try:
        print(f"Inserting data for {city} on {date}...")
        conn = pyodbc.connect(DB_CONNECTION_STRING)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO weather_data (city, date, temperature, humidity, pressure)
            VALUES (?, ?, ?, ?, ?)
        ''', (city, date, temperature, humidity, pressure))
        conn.commit()
        conn.close()
        print("Data inserted successfully.")
    except pyodbc.Error as e:
        print(f"Error inserting data: {e}")

def get_past_30_days():
    """Generate a list of dates for the past 30 days."""
    today = datetime.now()
    return [today - timedelta(days=i) for i in range(30)]


def get_min_max_values(city):
    """Get min and max temperature, humidity, and pressure for a city."""
    try:
        conn = pyodbc.connect(DB_CONNECTION_STRING)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT
                MIN(temperature) AS min_temp,
                MAX(temperature) AS max_temp,
                MIN(humidity) AS min_humidity,
                MAX(humidity) AS max_humidity,
                MIN(pressure) AS min_pressure,
                MAX(pressure) AS max_pressure
            FROM weather_data
            WHERE city = ?
        ''', (city,))
        result = cursor.fetchone()
        conn.close()
        return result
    except pyodbc.Error as e:
        print(f"Error fetching min/max values for {city}: {e}")
        return None

def get_average_values(city):
    """Get average temperature, humidity, and pressure for a city."""
    try:
        conn = pyodbc.connect(DB_CONNECTION_STRING)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT
                AVG(temperature) AS avg_temp,
                AVG(humidity) AS avg_humidity,
                AVG(pressure) AS avg_pressure
            FROM weather_data
            WHERE city = ?
        ''', (city,))
        result = cursor.fetchone()
        conn.close()
        return result
    except pyodbc.Error as e:
        print(f"Error fetching average values for {city}: {e}")
        return None
    
def get_comfortable_days(city):
    """Get the number of days with comfortable weather (temperature between 15°C and 25°C, humidity below 70%)."""
    try:
        conn = pyodbc.connect(DB_CONNECTION_STRING)
        cursor = conn.cursor()
        cursor.execute('''
            SELECT COUNT(*)
            FROM weather_data
            WHERE city = ?
            AND temperature BETWEEN 15 AND 25
            AND humidity < 70
        ''', (city,))
        result = cursor.fetchone()
        conn.close()
        return result[0]
    except pyodbc.Error as e:
        print(f"Error fetching comfortable days for {city}: {e}")
        return None

def main():
    """Main function to fetch and store weather data."""
    print("Starting main function...")
    cities = ["London", "New York", "Tokyo", "Sydney", "Berlin"]
    create_table()

    # Fetch and insert weather data
    for city in cities:
        for date in get_past_30_days():
            print(f"Processing {city} on {date.strftime('%Y-%m-%d')}...")
            data = fetch_weather_data(city, date.strftime("%Y-%m-%d"))
            if data and data.get("main"):
                insert_weather_data(
                    city,
                    date.strftime("%Y-%m-%d"),
                    data["main"]["temp"],
                    data["main"]["humidity"],
                    data["main"]["pressure"]
                )

    # Display analysis results
    for city in cities:
        print(f"\nWeather analysis for {city}:")
        
        # Min/Max Values
        min_max = get_min_max_values(city)
        if min_max:
            print(f"Min Temperature: {min_max.min_temp}°C")
            print(f"Max Temperature: {min_max.max_temp}°C")
            print(f"Min Humidity: {min_max.min_humidity}%")
            print(f"Max Humidity: {min_max.max_humidity}%")
            print(f"Min Pressure: {min_max.min_pressure} hPa")
            print(f"Max Pressure: {min_max.max_pressure} hPa")

        # Average Values
        avg_values = get_average_values(city)
        if avg_values:
            print(f"Average Temperature: {avg_values.avg_temp:.2f}°C")
            print(f"Average Humidity: {avg_values.avg_humidity:.2f}%")
            print(f"Average Pressure: {avg_values.avg_pressure:.2f} hPa")

        # Comfortable Days
        comfortable_days = get_comfortable_days(city)
        if comfortable_days is not None:
            print(f"Number of Comfortable Days: {comfortable_days}")

    print("Script completed.")

if __name__ == "__main__":
    main()