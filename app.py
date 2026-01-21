"""Weather application using Flask and Weather.gov API."""
from flask import Flask, jsonify, render_template
import requests
app = Flask(__name__)

@app.route('/')

def home():
    return render_template('index.html')

@app.route('/get-weather')
def get_weather():
    headers = {'User-Agent': 'MyWeatherApp'}
    point_res = requests.get("https://api.weather.gov/points/43.0481,-76.1474", headers=headers, timeout=10)
    points_data = point_res.json()
    
    forecast_url = points_data['properties']['forecast']
    weather_res = requests.get(forecast_url, headers=headers, timeout=10)
    weather_data = weather_res.json()
    
    current = weather_data['properties']['periods'][0]
    
    return jsonify({
        "temp":current['temperature'],
        "shortForecast": current['shortForecast'],
        "advice": "wear a coat!" if current['temperature'] < 50 else "T-Shirt time"
        })
    
if __name__ == '__main__':
        app.run(debug=True)