# Weather Data Analysis Project

This project fetches weather data for random cities around the world using the OpenWeatherMap API, stores the data in an Azure SQL Database, and performs analysis such as calculating min/max values, averages, and the number of comfortable days.

---

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Setup Instructions](#setup-instructions)
5. [Running the Project](#running-the-project)
6. [Analysis Output](#analysis-output)
7. [Troubleshooting](#troubleshooting)

---

## Project Overview

This project is designed to:
1. Fetch weather data for the past 30 days for a list of cities using the OpenWeatherMap API.
2. Store the data in an Azure SQL Database.
3. Perform analysis on the stored data, including:
   - Min/Max temperature, humidity, and pressure.
   - Average temperature, humidity, and pressure.
   - Number of "comfortable" days (temperature between 10°C and 30°C, humidity below 80%).

---

## Features

- **Data Fetching**: Fetches weather data for the past 30 days for multiple cities.
- **Data Storage**: Stores the fetched data in an Azure SQL Database.
- **Data Analysis**:
  - Calculates min/max values for temperature, humidity, and pressure.
  - Calculates average values for temperature, humidity, and pressure.
  - Determines the number of comfortable days based on user-defined criteria.
- **Error Handling**: Includes robust error handling for API calls and database operations.

---

## Prerequisites

Before running the project, ensure you have the following:

1. **Python 3.9 or higher**: Install Python from [python.org](https://www.python.org/).
2. **Azure Account**: Create a free Azure account at [Azure Free Account](https://azure.microsoft.com/free/).
3. **OpenWeatherMap API Key**: Sign up for a free API key at [OpenWeatherMap](https://openweathermap.org/api).
4. **Azure SQL Database**: Set up an Azure SQL Database and note the connection string.
5. **ODBC Driver**: Install the ODBC Driver 17 for SQL Server from [here](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server).

---

## Setup Instructions

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/weather-data-project.git
   cd weather-data-project
   ```

2. **Install Dependencies**:
   Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file in the project root directory and add the following:
   ```
   DB_CONNECTION_STRING=Driver={ODBC Driver 17 for SQL Server};Server=tcp:<server_name>,1433;Database=<database_name>;Uid=<username>;Pwd=<password>;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;
   API_KEY=your_openweathermap_api_key
   ```

4. **Set Up Azure SQL Database**:
   - Create a table in your Azure SQL Database using the following schema:
     ```sql
     CREATE TABLE weather_data (
         id INTEGER PRIMARY KEY IDENTITY(1,1),
         city NVARCHAR(100),
         date TEXT,
         temperature FLOAT,
         humidity FLOAT,
         pressure FLOAT
     );
     ```

---

## Running the Project

1. **Run the Script**:
   Execute the Python script to fetch and analyze weather data:
   ```bash
   python app.py
   ```

2. **View Output**:
   The script will print the analysis results to the console, including:
   - Min/Max values for temperature, humidity, and pressure.
   - Average values for temperature, humidity, and pressure.
   - Number of comfortable days.

---

## Analysis Output

The script generates the following analysis for each city:
- **Min/Max Values**:
  - Min Temperature
  - Max Temperature
  - Min Humidity
  - Max Humidity
  - Min Pressure
  - Max Pressure
- **Average Values**:
  - Average Temperature
  - Average Humidity
  - Average Pressure
- **Comfortable Days**:
  - Number of days with temperature between 10°C and 30°C and humidity below 80%.

---

## Troubleshooting

1. **Firewall Issues**:
   - Ensure your IP address is added to the Azure SQL Server firewall rules.
   - Follow the steps in the [Azure Firewall Documentation](https://learn.microsoft.com/en-us/azure/azure-sql/database/firewall-configure).

2. **Database Connection Issues**:
   - Verify the `DB_CONNECTION_STRING` in the `.env` file.
   - Ensure the ODBC Driver 17 for SQL Server is installed.

3. **API Key Issues**:
   - Ensure the `API_KEY` is valid and has access to the OpenWeatherMap API.

4. **Script Errors**:
   - Check the console output for error messages.
   - Add additional `print` statements for debugging.

---

## Acknowledgments

- [OpenWeatherMap](https://openweathermap.org/) for providing the weather data API.
- [Microsoft Azure](https://azure.microsoft.com/en-us/)
