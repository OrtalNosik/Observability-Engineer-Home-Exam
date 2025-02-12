import os
import pyodbc

DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")
if not DB_CONNECTION_STRING:
    raise ValueError("DB_CONNECTION_STRING environment variable is not set.")

print("Starting script...")

def fetch_weather_data(city, date):
    print(f"Fetching weather data for {city} on {date}...")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&dt={date}"
    response = requests.get(url)
    print(f"Response status code: {response.status_code}")
    return response.json()

def create_table():
    print("Creating table...")
    conn = pyodbc.connect(DB_CONNECTION_STRING)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_data (
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
    print("Table created.")

def insert_weather_data(city, date, temperature, humidity, pressure):
    print(f"Inserting data for {city} on {date}...")
    conn = pyodbc.connect(DB_CONNECTION_STRING)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO weather_data (city, date, temperature, humidity, pressure)
        VALUES (?, ?, ?, ?, ?)
    ''', (city, date, temperature, humidity, pressure))
    conn.commit()
    conn.close()
    print("Data inserted.")

def main():
    print("Starting main function...")
    cities = ["London", "New York", "Tokyo", "Sydney", "Berlin"]
    create_table()

    for city in cities:
        for date in get_past_30_days():
            print(f"Processing {city} on {date.strftime('%Y-%m-%d')}...")
            data = fetch_weather_data(city, date.strftime("%Y-%m-%d"))
            if data.get("main"):
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