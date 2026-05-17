from collections import defaultdict
from datetime import datetime
import requests
from requests import api

class WeatherService:
    def __init__(self, api_key) -> None:
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def get_current_weather(self,city:str):
        params = {
            "q" : city,
            "appid": self.api_key,
            "units": "metric"
        }

        try:
            response = requests.get(
                self.base_url,
                params=params,
                timeout=5
            )

            response.raise_for_status()

            data = response.json()

            weather_data = {
                "city" : data["name"],
                "temperature": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"],
                "wind_speed": data["wind"]["speed"],
                "icon" : data["weather"][0]["icon"],
            
            }
            return weather_data

        except requests.exceptions.Timeout:
            return {
                "error": "Request timed out"
            }

        except requests.exceptions.HTTPError:

            if response.status_code == 404:
                return {
                    "error": "City not found"
                }

            return {
                "error": "HTTP error occurred"
            }

        except requests.exceptions.RequestException:
            return {
                "error": "Connection error"
            }

        except KeyError:
            return {
                "error": "Invalid API response"
            }

    def get_forecast(self, city: str):

        forecast_url = "https://api.openweathermap.org/data/2.5/forecast"

        params = {
        "q": city,
        "appid": self.api_key,
        "units": "metric"
    }

        response = requests.get(forecast_url, params=params, timeout=5)
        response.raise_for_status()

        data = response.json()

        today = []
        daily_map = defaultdict(list)

        for item in data["list"]:

            dt = datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S")

            # TODAY (next 24h, by hour)
            today.append({
                "time": dt.strftime("%H:%M"),
                "temp": item["main"]["temp"],
                "icon": item["weather"][0]["icon"]
            })

            # GROUP BY DAY
            day_key = dt.strftime("%Y-%m-%d")

            daily_map[day_key].append(item)

        daily = []

        for day, items in daily_map.items():

            temps = [i["main"]["temp"] for i in items]

            daily.append({
                "date": day,
                "min": min(temps),
                "max": max(temps),
                "icon": items[0]["weather"][0]["icon"],
                "description": items[0]["weather"][0]["description"]
            })

        return {
            "today": today[:8],   # limit hours
            "daily": daily[:5]
        }