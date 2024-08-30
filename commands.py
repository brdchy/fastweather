import requests 
import json 
from datetime import datetime
from secret import WEATHER_API_KEY
from weather_description import categorize_weather_description

# Weather source 1
def get_weather_wttr(): 
    url = f"https://wttr.in/Vladivostok?format=j1" 
    response = requests.get(url) 
    result = {}
    if response.status_code == 200: 
        data = response.json() 
        with open(f"Vladivostok_weather_1.json", "w", encoding="utf-8") as file: 
            json.dump(data, file, ensure_ascii=False, indent=4) 
        times = ["00:00:00", "03:00:00", "06:00:00", "09:00:00", "12:00:00", "15:00:00", "18:00:00", "21:00:00"]
        time_index = 0

        for day in data['weather']:
            date = day['date']
            result[date] = []
            for weather_data in day['hourly']:
                datetime_str = f"{date} {times[time_index]}"
                time_index = (time_index + 1) % len(times)
                formatted_result = { 
                            "date_time": datetime_str,   
                            "temperature": float(weather_data["tempC"]), 
                            "feels_like": float(weather_data["FeelsLikeC"]), 
                            "description": categorize_weather_description(weather_data["weatherDesc"][0]["value"]), 
                            "humidity": int(weather_data["humidity"]), 
                            "wind_speed": int(weather_data["windspeedKmph"]), 
                            "wind_direction": weather_data["winddir16Point"], 
                            "pressure": int(weather_data["pressure"]), 
                            "precipitation": float(weather_data["precipMM"]), 
                            "uv_index": int(weather_data["uvIndex"]), 
                            "source": "wttr.in" 
                        } 
                result[date].append(formatted_result) 
        return result
    else: 
        return 0


# Weather source 2
def get_weather_weatherapi():
    latitude = 43.02632103759889
    longitude = 131.89011940838617
    url = f'https://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={latitude},{longitude}&days=3&aqi=no&alerts=no'
    response = requests.get(url)
    result = {}
    if response.status_code == 200:
        data = response.json()
        with open(f"Vladivostok_weather_3.json", "w", encoding="utf-8") as file: 
            json.dump(data, file, ensure_ascii=False, indent=4) 
        for forecastday in data["forecast"]["forecastday"]:
            date = forecastday["date"]
            result[date] = []
            for weather_data in forecastday["hour"]:
                hour = int(weather_data["time"].split()[1].split(':')[0])
                if hour % 3 == 0:
                    formatted_result = {
                        "date_time": weather_data["time"]+':00',
                        "temperature": weather_data["temp_c"],
                        "feels_like": weather_data["feelslike_c"],
                        "description": categorize_weather_description(weather_data["condition"]["text"].strip()),
                        "humidity": weather_data["humidity"],
                        "wind_speed": weather_data["wind_kph"],
                        "wind_direction": weather_data["wind_dir"],
                        "pressure": weather_data["pressure_mb"],
                        "precipitation": weather_data["precip_mm"],
                        "uv_index": weather_data["uv"],
                        "source": "Weather API"
                    }
                    result[date].append(formatted_result)
        return result
    else:
        return 0
 
def get_current_weather_wttr(): 
    url = f"https://wttr.in/Vladivostok?format=j1" 
    response = requests.get(url) 
    if response.status_code == 200: 
        data = response.json()['current_condition'][0]
        local_obs_datetime = datetime.strptime(data["localObsDateTime"], "%Y-%m-%d %I:%M %p")
        local_obs_datetime_24h = local_obs_datetime.strftime("%Y-%m-%d %H:%M")
        result = {
            "date_time": local_obs_datetime_24h,
            "temperature": float(data['temp_C']),
            "feels_like": float(data['FeelsLikeC']),
            "description": categorize_weather_description(data["weatherDesc"][0]["value"]),
            "humidity": float(data['humidity']),
            "wind_speed": float(data['windspeedKmph']),
            "wind_direction": data["winddir16Point"],
            "pressure": float(data['pressure']),
            "precipitation": float(data['precipMM']),
            "uv_index": float(data["uvIndex"]) if data["uvIndex"] else None,
            "source": "wttr.in"
        }
        return result
    else: 
        return None
    
def get_current_weather_weatherapi():
    latitude = 43.02632103759889
    longitude = 131.89011940838617
    url = f'http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={latitude},{longitude}&days=3&aqi=no&alerts=no'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()['current']
        result = {
            "date_time": data["last_updated"],
            "temperature": float(data['temp_c']),
            "feels_like": float(data['feelslike_c']),
            "description": categorize_weather_description(data["condition"]["text"]),
            "humidity": float(data['humidity']),
            "wind_speed": float(data['wind_kph']),
            "wind_direction": data["wind_dir"],
            "pressure": float(data['pressure_mb']),
            "precipitation": float(data['precip_mm']),
            "uv_index": float(data["uv"]) if data["uv"] else None,
            "source": "Weather API"
        }
        return result
    else:
        return None
    