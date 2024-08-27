import requests 
import json 
from datetime import datetime
from secret import WEATHER_API_KEY
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
                            "Дата/Время": datetime_str,   
                            "Температура": float(weather_data["tempC"]), 
                            "Ощущается как": float(weather_data["FeelsLikeC"]), 
                            "Описание": weather_data["weatherDesc"][0]["value"], 
                            "Влажность": int(weather_data["humidity"]), 
                            "Скорость ветра": int(weather_data["windspeedKmph"]), 
                            "Направление ветра": weather_data["winddir16Point"], 
                            "Давление": int(weather_data["pressure"]), 
                            "Осадки": float(weather_data["precipMM"]), 
                            "UV-индекс": int(weather_data["uvIndex"]), 
                            "Источник": "wttr.in" 
                        } 
                result[date].append(formatted_result) 
        return result
    else: 
        return 0


# Weather source 2
def get_weather_weatherapi():
    url = f'http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}8&q=Vladivostok&days=3&aqi=no&alerts=no'
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
                        "Дата/Время": weather_data["time"]+':00',
                        "Температура": weather_data["temp_c"],
                        "Ощущается как": weather_data["feelslike_c"],
                        "Описание": weather_data["condition"]["text"].strip(),
                        "Влажность": weather_data["humidity"],
                        "Скорость ветра": weather_data["wind_kph"],
                        "Направление ветра": weather_data["wind_dir"],
                        "Давление": weather_data["pressure_mb"],
                        "Осадки": weather_data["precip_mm"],
                        "UV-индекс": weather_data["uv"],
                        "Источник": "WeatherAPI"
                    }
                    result[date].append(formatted_result)
        return result
    else:
        return 0
 
def get_current_weather_wttr(): 
    url = f"https://wttr.in/Vladivostok?format=j1" 
    response = requests.get(url) 
    result = {}
    if response.status_code == 200: 
        data = response.json()['current_condition'][0]
        local_obs_datetime = datetime.strptime(data["localObsDateTime"], "%Y-%m-%d %I:%M %p")
        local_obs_datetime_24h = local_obs_datetime.strftime("%Y-%m-%d %H:%M")
        result = {
            "Дата/Время": local_obs_datetime_24h,
            "Температура": f"{data['temp_C']}",
            "Ощущается как": f"{data['FeelsLikeC']}",
            "Описание": data["weatherDesc"][0]["value"],
            "Влажность": f"{data['humidity']}",
            "Скорость ветра": f"{data['windspeedKmph']}",
            "Направление ветра": data["winddir16Point"],
            "Давление": f"{data['pressure']}",
            "Осадки": f"{data['precipMM']}",
            "UV-индекс": data["uvIndex"],
            "Источник": "wttr.in"
        }
        return result
    else: 
        return 0
    
def get_current_weather_weatherapi():
    url = f'http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q=Vladivostok&days=3&aqi=no&alerts=no'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()['current']
        result = {
            "Дата/Время": data["last_updated"],
            "Температура": f"{data['temp_c']}",
            "Ощущается как": f"{data['feelslike_c']}",
            "Описание": data["condition"]["text"],
            "Влажность": f"{data['humidity']}%",
            "Скорость ветра": f"{data['wind_kph']}",
            "Направление ветра": data["wind_dir"],
            "Давление": f"{data['pressure_mb']}",
            "Осадки": f"{data['precip_mm']}",
            "UV-индекс": data["uv"],
            "Источник": "Weather API"
        }
        return result
    else:
        return 0  
    
print(get_current_weather_weatherapi())    