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
    
    all_periods = weather_data['properties']['periods']
    
    forecast_list = []
    
    for period in all_periods:
        if period['isDaytime']:
            forecast_list.append({
                "name": period['name'],
                "temp": period['temperature'],
                "icon": period['icon'],
                "short": period['shortForecast']
            })
        if len(forecast_list) == 5:
            break
    
    current = all_periods[0]
    
    temp = current['temperature']
    forecast_text = current ['shortForecast'].lower()
    wind_numbers = current['windSpeed'].split()[0]
    
    try:
        wind_val = int(wind_numbers)
    except ValueError:
        wind_val = 0 #safety check

    if temp < 32:
        advice = "Freezing out there! wear a good heavy coat, boot and gloves. <br>"
        color = "#a2d2ff"
    elif temp < 60:
        advice = "chilly! wear a jacket or sweatshirt. <br>"
        color = "#fefae0"
    else:
        advice = "warm out, T-Shirt will suffice. <br>"
        color = "#ffb703"
        
    if wind_val > 20:
        advice += "High Winds! it'll be much colder than what the forecast says, be prepared!"
    elif wind_val > 10:
        advice += "A little bit Windy today."

    if "snow" in forecast_text:
        advice+= "Also, Watch out for snow! you should probably wear some waterproof shoes."
    elif "rain" in forecast_text or "showers" in forecast_text:
        advice += "Looks Like Rain, you should bring an umbrella or a raincoat."
    print(f"DEBUG: The whole dictionary looks like this: {current}")
    
            
            
            
            
    return jsonify({
        "temp": temp,
        "icon": current['icon'],
        "shortForecast": current['shortForecast'],
        "wind": f"{current['windSpeed']} {current['windDirection']}",
        "advice": advice,
        "color": color,
        "five_day": forecast_list
        })
    
if __name__ == '__main__':
    app.run(debug=True)