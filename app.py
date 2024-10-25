from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests
from datetime import datetime
import pymysql

app = Flask(__name__)
app.secret_key = 'weather_app_secret'

# OpenWeatherMap API Key
API_KEY = '8240c4855f16f667d201a939883de936'  # Replace with your OpenWeatherMap API key

# Cities to track
CITIES = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']

# MySQL Database Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345',
    'db': 'weather_db',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# Connect to the MySQL database
def get_db_connection():
    conn = pymysql.connect(**db_config)
    return conn

# Create the necessary database tables if not exist
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS weather_summary (
        id INT AUTO_INCREMENT PRIMARY KEY,
        city VARCHAR(255),
        date DATE,
        avg_temp FLOAT,
        max_temp FLOAT,
        min_temp FLOAT,
        dominant_condition VARCHAR(255)
    )''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS alerts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        city VARCHAR(255),
        threshold FLOAT,
        triggered_at DATETIME
    )''')

    conn.commit()
    conn.close()

# Fetch weather data from OpenWeatherMap
def get_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Fetch and aggregate weather data
def fetch_weather_and_save_summary():
    conn = get_db_connection()
    cursor = conn.cursor()

    for city in CITIES:
        data = get_weather_data(city)
        if data:
            temp = data['main']['temp']
            max_temp = data['main']['temp_max']
            min_temp = data['main']['temp_min']
            weather_condition = data['weather'][0]['main']

            cursor.execute(
                '''INSERT INTO weather_summary (city, date, avg_temp, max_temp, min_temp, dominant_condition) 
                VALUES (%s, %s, %s, %s, %s, %s)''',
                (city, datetime.now().strftime('%Y-%m-%d'), temp, max_temp, min_temp, weather_condition)
            )
    conn.commit()
    conn.close()

# Set up alert thresholds
@app.route('/set_alert', methods=['POST'])
def set_alert():
    city = request.form['city']
    threshold = float(request.form['threshold'])
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO alerts (city, threshold, triggered_at) VALUES (%s, %s, %s)', 
                   (city, threshold, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()
    
    flash(f"Alert set for {city} at threshold {threshold}°C", 'success')
    return redirect(url_for('index'))

# Route to display the index page with real-time weather data and summaries
@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Fetch weather summaries
    cursor.execute('SELECT * FROM weather_summary ORDER BY date DESC')
    weather_summaries = cursor.fetchall()

    # Fetch alert thresholds
    cursor.execute('SELECT * FROM alerts')
    alerts = cursor.fetchall()

    # Fetch real-time weather data
    weather_data = {}
    for city in CITIES:
        data = get_weather_data(city)
        if data:
            weather_data[city] = {
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'weather': data['weather'][0]['description']
            }
        else:
            weather_data[city] = {'error': 'Could not retrieve data'}

    conn.close()

    return render_template('index.html', weather_data=weather_data, summaries=weather_summaries, alerts=alerts)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
