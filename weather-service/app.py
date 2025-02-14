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

def main():
    """Main function to fetch and store weather data."""
    print("Starting main function...")
    cities = ["London", "New York", "Tokyo", "Sydney", "Berlin"]
    create_table()

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
    print("Script completed.")

if __name__ == "__main__":
    main()