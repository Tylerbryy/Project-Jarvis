import requests
import json
from keys import *

weather_api_key = WEATHER_API_KEY
city_name = CITY_NAME
lat = YOUR_LATITUDE
lon = YOUR_LONGITUDE

url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_api_key}"
response = requests.get(url)
weather_data = response.json()

def get_weather_info(weather_dict):
    # Extract the relevant weather information
    weather_info = []
    for key, value in weather_dict.items():
        if key == 'weather':
            weather_info.append('Weather:')
            for item in value:
                weather_info.append(f"- {item['main']}: {item['description']}")
        elif key == 'main':
            weather_info.append('Temperature:')
            temp_min_fahrenheit = round((value['temp_min'] - 273.15) * 9/5 + 32)
            temp_max_fahrenheit = round((value['temp_max'] - 273.15) * 9/5 + 32)
            weather_info.append(f"- Min: {temp_min_fahrenheit} F")
            weather_info.append(f"- Max: {temp_max_fahrenheit} F")
            weather_info.append(f"- Pressure: {value['pressure']} hPa")
            weather_info.append(f"- Humidity: {value['humidity']}%")
    
    # Join the weather information into a formatted string
    weather_str = '\n'.join(weather_info)
    return weather_str

