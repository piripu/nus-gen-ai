import requests, config, dotenv, json, logging
from helpers import Result, Weather, ListJSONEncoder

dotenv.load_dotenv()

logger = logging.getLogger(__name__)

def get_current_weather(location) -> Result[Weather]:
    try: 
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}" 
        params = { 
            "key": config.VISUAL_CROSSING_API_KEY, 
            "unitGroup": "metric", 
            "include": "days,current",
            "contentType": "json"
        }
        logger.debug(f"Getting for: {url}")
        response = requests.get(url, params=params) 
        logger.debug(f"Result status code: {response.status_code}")
        # Handle invalid API key error
        if response.status_code == 401:
            return Result(success=False, error="Invalid API Key")
        
        if response.status_code == 400:
            return Result(success=False, error=response.json())
        
        # Raise exception for bad status codes other than 401
        response.raise_for_status() 
        
        response_json = response.json()
        current = response_json.get("days", [{}])[0]

        weather = Weather(
            location = response_json.get("resolvedAddress", ""),
            temp_celsius=current.get("temp", 0.0),
            humidity=current.get("humidity", 0),
            condition=current.get("conditions", ""),
            description=current.get("description", "")
        )
        logger.debug("Result: %s", weather)
        return Result(success=True, data=weather)
    except requests.exceptions.RequestException as e:
        # Return a failure result with error message
        return Result(success=False, error=str(e))
    
def get_forecast_weather(location) -> Result[list[Weather]]:
    try: 
        url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}" 
        params = { 
            "key": config.VISUAL_CROSSING_API_KEY, 
            "unitGroup": "metric", 
            "include": "days,current",
            "contentType": "json"
        }
        logger.debug(f"Getting for: {url}")
        response = requests.get(url, params=params) 
        logger.debug(f"Result status code: {response.status_code}")
        # Handle invalid API key error
        if response.status_code == 401:
            return Result(success=False, error="Invalid API Key")
        
        if response.status_code == 400:
            return Result(success=False, error=response.json())
        
        # Raise exception for bad status codes other than 401
        response.raise_for_status() 
        
        response_json = response.json()
        days = response_json.get("days", [{}])
        forecast = [
            Weather(
                location = response_json.get("resolvedAddress", ""),
                temp_celsius=day.get("temp", 0.0),
                humidity=day.get("humidity", 0),
                condition=day.get("conditions", ""),
                description=day.get("description", "")
            )
            for day in days
        ]
        logger.debug("Result: %s", json.dumps(forecast, cls=ListJSONEncoder))
        return Result(success=True, data=forecast)
    except requests.exceptions.RequestException as e:
        # Return a failure result with error message
        return Result(success=False, error=str(e))