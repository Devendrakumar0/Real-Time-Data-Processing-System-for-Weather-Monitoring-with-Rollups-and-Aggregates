# Real-Time-Data-Processing-System-for-Weather-Monitoring-with-Rollups-and-Aggregates

# Indian Metro Cities Weather Monitoring Dashboard 🌦️

This Flask-based project monitors real-time weather conditions in major Indian metro cities using the OpenWeatherMap API. It provides summarized daily weather insights, configurable alerts, and displays weather data in a responsive, user-friendly web interface.

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)


---

## Features

- **Real-Time Weather Monitoring**: Retrieve and display current weather conditions every 5 minutes.
- **Daily Weather Summary**: Roll up daily weather data, including average, max, and min temperatures, and dominant conditions.
- **Custom Alerts**: Set and receive alerts when certain weather conditions or temperature thresholds are met.
- **Responsive Design**: Mobile-friendly interface for easy accessibility on any device.
- **Optional Forecast Support**: Extendable to show additional weather parameters and forecasts.

---

## Requirements

- Python 3.7+
- Flask
- `pymysql` connector
- OpenWeatherMap API key (Free API key can be obtained at https://openweathermap.org/)

---

## Installation
- pip install flask
- pip install pymysql
- Setup MySQL Database
      Start MySQL and create a database for the project.


## USAGE
- Access the Web Interface Open your browser and go to http://localhost:5000.

- Set Alerts You can set temperature alerts by selecting a city and specifying a threshold in Celsius. Alerts will trigger if the threshold is exceeded.

- View Daily Summaries Check daily weather summaries for each city, including temperature trends and dominant weather conditions.

## Configuration

- API Call Interval: Modify the API call interval to change how frequently weather data is fetched. The default interval is set to 5 minutes.
- Additional Parameters: Extend the application to support more weather parameters like humidity and wind speed by updating the API requests and database schema.

## Project Structure


├── app.py               # Main application logic
├── static/
│   └── styles.css       # Styling for the web interface
├── templates/
│   └── index.html       # Main HTML page
├── README.md            # Project documentation


## API Documentation
- GET /
      Fetch and display real-time weather data and daily summaries for all cities.

- POST /set_alert
      Set a weather alert with a city and a temperature threshold.


