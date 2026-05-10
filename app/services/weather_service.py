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