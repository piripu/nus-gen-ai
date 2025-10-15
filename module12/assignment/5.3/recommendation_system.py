import openai 
import requests 
import sqlite3 
from datetime import datetime 
from config import OPENAI_API_KEY, WEATHER_API_KEY 

# Use result pattern to safely return data or error
# We'll handle errors gracefully in the function call
class Result:
    def __init__(self, success, data=None, error=None):
        self.success = success
        self.data = data
        self.error = error

class WeatherAgent: 
    def __init__(self, api_key): 
        self.api_key = api_key 
    
    # p.esguerra: Kind of challenging to get as the api needs to use forecast for future dates below 14 days
    #      with the same API, it throws in a massive JSON response
    #      For simplicity, we'll just use current weather and future dates within 14 days as of writing this code
    #      It'll be great if we have a better weather API for forecast data
    def get_weather(self, location, date): 
        # Use current weather since we're dealing with same-day recommendations 
        # url = f"http://api.weatherapi.com/v1/current.json" 
        url = f"http://api.weatherapi.com/v1/forecast.json"
        
        params = { 
            "key": self.api_key, 
            "q": location, 
            "days": 14,   # Get forecast for up to 14 days
            "aqi": "no" 
        } 
        try: 
            response = requests.get(url, params=params)
            # Handle invalid API key error
            if response.status_code == 401:
                return Result(success=False, error="Invalid API Key")

            if response.status_code == 400:
                return Result(success=False, error=response.json()['error']['message'])
        
            response.raise_for_status()
            
            # p.esguerra: Extract forecast for the specific date if available
            forecast_day = response.json()
            if 'forecast' in forecast_day and 'forecastday' in forecast_day['forecast']:
                for day in forecast_day['forecast']['forecastday']:
                    if day['date'] == date:
                        return Result(success=True, data=day['day'])

            return Result(success=False, error="No forecast data available for the specified date.")

        except requests.exceptions.RequestException as e:
            # Return a failure result with error message
            return Result(success=False, error=str(e))
 
class EventAgent: 
    def get_events(self, date, event_type=None): 
        conn = sqlite3.connect('events.db') 
        c = conn.cursor() 
         
        try: 
            if event_type: 
                c.execute('SELECT * FROM events WHERE date = ? AND type = ?', (date, event_type)) 
            else: 
                c.execute('SELECT * FROM events WHERE date = ?', (date,)) 
                 
            events = c.fetchall() 
            return events 
        except sqlite3.Error as e: 
            raise Exception(f"Database error: {str(e)}") 
        finally: 
            conn.close() 
 
class RecommendationAgent: 
    def __init__(self, openai_api_key): 
        self.api_key = openai_api_key 
        openai.api_key = openai_api_key 
     
    def generate_recommendation(self, date, weather_data, events): 
        # Create context for GPT 
        try:
            context = f"Date: {date}\n\n"
            
            # p.esguerra: Handle errors in weather data
            if weather_data.success:
                weather_condition = weather_data.data['condition']['text'] 
                temperature = weather_data.data['avgtemp_c'] 
                context += f"Weather: {weather_condition}, Temperature: {temperature}°C\n\n" 
            else:
                context += "Weather data unavailable: " + weather_data.error + "\n\n"
             
            context += "Available events:\n" 
            for event in events: 
                context += f"- {event[1]} ({event[2]}): {event[3]} at {event[4]}\n" 
             
            response = openai.ChatCompletion.create( 
                model="gpt-4", 
                messages=[ 
                    {"role": "system", "content": """You are a helpful event recommender. Consider the weather conditions  
                    and suggest suitable events. For outdoor events, consider the temperature and weather conditions. 
                    Be specific about why you recommend certain events over others. Keep your response concise but informative. 
                    If weather data is unavailable, focus on providing a balanced recommendation of both indoor and outdoor events."""}, 
                    {"role": "user", "content": context} 
                ] 
            ) 
            return response.choices[0].message.content 
        except Exception as e: 
            raise Exception(f"Recommendation error: {str(e)}") 
 
class CoordinatorAgent: 
    def __init__(self, weather_api_key, openai_api_key): 
        self.weather_agent = WeatherAgent(weather_api_key) 
        self.event_agent = EventAgent() 
        self.recommendation_agent = RecommendationAgent(openai_api_key) 
     
    def get_recommendations(self, location, date): 
        try: 
            # Get weather data 
            print(f"\nFetching weather data for {location} on {date}...") 
            weather_data = self.weather_agent.get_weather(location, date) 
            
            # Get events 
            print("Fetching events...") 
            events = self.event_agent.get_events(date) 
             
            if not events: 
                return "No events found for this date." 
             
            # Generate recommendations 
            print("Generating recommendations...") 
            recommendations = self.recommendation_agent.generate_recommendation( 
                date, weather_data, events 
            ) 
             
            return recommendations 
             
        except Exception as e: 
            return f"Error: {str(e)}" 
 
if __name__ == "__main__": 
    # Test dates 
    test_cases = [ 
        ("2025-10-15", "Philippines"), 
        ("2025-10-16", "Philippines"), 
        ("2025-10-17", "Philippines"), 
        ("2025-10-18", "xAE"),              # Invalid location
        ("2025-12-21", "Philippines")       # No events on this date
    ] 
     
    coordinator = CoordinatorAgent(WEATHER_API_KEY, OPENAI_API_KEY) 
     
    for test_date, test_location in test_cases: 
        print(f"\n{'='*50}") 
        print(f"Getting recommendations for {test_location} on {test_date}:") 
        print(f"{'='*50}") 
        print(coordinator.get_recommendations(test_location, test_date)) 