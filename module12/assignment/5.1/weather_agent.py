import requests, openai, json
from config import WEATHER_API_KEY 
from config import OPENAI_API_KEY 

# Use result pattern to safely return data or error
# We'll handle errors gracefully in the function call
class Result:
    def __init__(self, success, data=None, error=None):
        self.success = success
        self.data = data
        self.error = error

def get_weather(location): 
    try: 
        url = f"http://api.weatherapi.com/v1/current.json" 
        params = { 
            "key": WEATHER_API_KEY, 
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
         
        return Result(success=True, data=response.json()) 
    except requests.exceptions.RequestException as e:
        # Return a failure result with error message
        return Result(success=False, error=str(e))

openai.api_key = OPENAI_API_KEY 
 
# Define the function that OpenAI can call 
functions = [ 
    { 
        "name": "get_weather", 
        "description": "Get current weather for a location", 
        "parameters": { 
            "type": "object", 
            "properties": { 
                "location": { 
                    "type": "string", 
                    "description": "City name or location" 
                } 
            }, 
            "required": ["location"] 
        } 
    } 
]

def weather_agent(user_query): 
    try: 
        # Get function call from OpenAI 
        response = openai.ChatCompletion.create( 
            model="gpt-4", 
            messages=[{"role": "user", "content": user_query}], 
            functions=functions, 
            function_call="auto" 
        ) 
         
        # Extract function call 
        function_call = response.choices[0].message.function_call
        
        # Execute function 
        if function_call.name == "get_weather": 
            # Parse the arguments from JSON string  
            arguments = json.loads(function_call.arguments)
            
            weather_data = get_weather(arguments["location"])
            
            if not weather_data.success:
                # if failure, return an error property
                return {
                    "error": weather_data.error
                }
            
            # if success, return the weather data
            return {
                "location": weather_data.data['location']['name'],
                "last_updated": weather_data.data['current']['last_updated'],
                "temperature_celcius": weather_data.data['current']['temp_c'],
                "temperature_fahrenheit": weather_data.data['current']['temp_f'],
                "humidity": weather_data.data['current']['humidity'],
                "condition": weather_data.data['current']['condition']['text']
            }
            
    except Exception as e: 
        return f"Error: {str(e)}" 

if __name__ == "__main__": 
    test_queries = [ 
        "What's the weather like in Singapore?", 
        "Is it raining in London right now?", 
        "Tell me the temperature in New York",
        "What's the weather like in xAE?", # Invalid location test
    ] 
     
    for query in test_queries: 
        print(f"\nQuery: {query}") 
        print(f"Response: {weather_agent(query)}") 