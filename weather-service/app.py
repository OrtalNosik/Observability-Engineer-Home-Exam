import os
import requests
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

# Load environment variables
API_KEY = os.getenv("API_KEY") 
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "weatherdb")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "password")

# Establish database connection
conn = psycopg2.connect(
    dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST
)

def create_table():
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS weather (
                id SERIAL PRIMARY KEY,
                city TEXT,
                temperature FLOAT,
                humidity INT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

create_table()

def fetch_weather(city):
    """Fetch weather from API and store in the database."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "Failed to fetch weather data", "status_code": response.status_code}

    data = response.json()

    if "main" not in data:
        return {"error": "Invalid API response"}

    temp = data["main"]["temp"]
    humidity = data["main"]["humidity"]

    # Store data in the database
    with conn.cursor() as cur:
        cur.execute("INSERT INTO weather (city, temperature, humidity) VALUES (%s, %s, %s)", 
                    (city, temp, humidity))
        conn.commit()

    return {"city": city, "temperature": temp, "humidity": humidity}

@app.route("/weather/<city>")
def get_weather(city):
    return jsonify(fetch_weather(city))

@app.route("/weather/stats")
def get_stats():
    """Get min, max, and average temperature stats from DB."""
    with conn.cursor() as cur:
        cur.execute("SELECT MIN(temperature), MAX(temperature), AVG(temperature) FROM weather")
        min_temp, max_temp, avg_temp = cur.fetchone()

    return jsonify({
        "min_temp": min_temp,
        "max_temp": max_temp,
        "avg_temp": avg_temp
    })

@app.route("/health")
def health_check():
    """Simple health check endpoint."""
    return jsonify({"status": "OK"}), 200

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000, debug=True)  # Debug mode for development
    finally:
        conn.close()  # Close database connection when the app stops
