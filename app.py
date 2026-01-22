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
    
    temp = current['temperature']

    if temp < 32:
        advice = "Freezing out there! wear a good heavy coat, boot and gloves."
        color = "#a2d2ff"
    elif temp < 60:
        advice = "chilly! wear a jacket or sweatshirt"
        color = "#fefae0"
    else:
        advice = "warm out, T-Shirt will suffice"
        color = "#ffb703"
            
            
            
            
            
    return jsonify({
        "temp": temp,
        "icon": current['icon'],
        "shortForecast": current['shortForecast'],
        "advice": advice,
        "color": color
        })
    
if __name__ == '__main__':
    app.run(debug=True)