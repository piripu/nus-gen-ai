import requests, config, dotenv, json
from helpers import Result, Weather

dotenv.load_dotenv()

def get_current_weather(location) -> Result[Weather]:
    try: 
        url = f"http://api.weatherapi.com/v1/current.json" 
        params = { 
            "key": config.WEATHER_API_KEY, 
            "q": location, 
            "aqi": "no" 
        } 
        response = requests.get(url, params=params) 
        
        # Handle invalid API key error
        if response.status_code == 401:
            return Result(success=False, error="Invalid API Key")
        
        if response.status_code == 400:
            return Result(success=False, error=response.json())
        
        # Raise exception for bad status codes other than 401
        response.raise_for_status() 
        
        response_json = response.json()
        weather = Weather(
            location=response_json.get("location", {}).get("name", ""),
            last_updated=response_json.get("current", {}).get("last_updated", ""),
            temp_celsius=response_json.get("current", {}).get("temp_c", 0.0),
            temp_fahrenheit=response_json.get("current", {}).get("temp_f", 0.0),
            humidity=response_json.get("current", {}).get("humidity", 0),
            condition=response_json.get("current", {}).get("condition", {}).get("text", "")
        )

        return Result(success=True, data=weather)
    except requests.exceptions.RequestException as e:
        # Return a failure result with error message
        return Result(success=False, error=str(e))
    
def get_forecast_weather(location) -> Result[dict]:
    try: 
        url = f"http://api.weatherapi.com/v1/forecast.json" 
        params = { 
            "key": config.WEATHER_API_KEY, 
            "q": location, 
            "days": 14,
            "aqi": "no",
            "alerts": "no"
        } 
        response = requests.get(url, params=params) 
        
        # Handle invalid API key error
        if response.status_code == 401:
            return Result(success=False, error="Invalid API Key")
        
        if response.status_code == 400:
            return Result(success=False, error=response.json())
        
        # Raise exception for bad status codes other than 401
        response.raise_for_status() 
        
        response_json = response.json()
        forecast_data = response_json.get("forecast", {})
        
        return Result(success=True, data=forecast_data)
    except requests.exceptions.RequestException as e:
        # Return a failure result with error message
        return Result(success=False, error=str(e))
