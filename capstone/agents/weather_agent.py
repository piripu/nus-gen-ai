from typing import Annotated, Literal
from haystack.components.agents import Agent
from haystack.dataclasses import ChatMessage
from haystack.tools import tool
from haystack.tools.tool import Tool

import helpers.weather_visual_crossing as weather
from helpers import ListJSONEncoder
from helpers.factory import create_chat_generator

import logging, json
logger = logging.getLogger(__name__)

@tool
def get_current_weather(
    location: Annotated[str, "REQUIRED: the city for which to get the weather"]):
    '''Get the current weather for a location.'''
    try:
        result = weather.get_current_weather(location)
        logger.debug("Weather fetch result: %s", result.data.to_dict())

        if result.success:
            return result.data
        else:
            return result.error
    except Exception as e:
        logger.error(f"Error getting weather for {location}: {e}")
        return f"Could not retrieve weather data for {location}."
    
@tool
def get_forecast_weather(
    location: Annotated[str, "REQUIRED: the city for which to get the weather"]):
    '''Get the weather forecast for a location for the next 15 days from current date.'''
    try:
        result = weather.get_forecast_weather(location)
        logger.debug("Weather fetch result: %s", json.dumps(result.data, cls=ListJSONEncoder))

        if result.success:
            return result.data
        else:
            return result.error
    except Exception as e:
        logger.error(f"Error getting weather for {location}: {e}")
        return f"Could not retrieve weather data for {location}."

class WeatherAgent(Agent):
    def __init__(self):
        super().__init__(
            chat_generator=create_chat_generator(),
            system_prompt="""You are a weather information agent. Use the tools available to provide accurate weather data.
            Ask for the user's location if it's not provided yet.""",
            tools=[get_current_weather, get_forecast_weather])
        
# We create a tool wrapper for the weather agent that only takes a message as input
class WeatherAgentTool(Tool):
    name = "weather_agent_tool"
    description = "A tool that provides weather information based on user queries. Location is REQUIRED. Ask for the user's location if it is not provided yet."

    def __init__(self):
        self.agent = WeatherAgent()
        
        super().__init__(
            name=self.name,
            description=self.description,
            parameters = {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Request message to get weather information for a specific location. Location is required. Date and time may be included when possible."
                    }
                },
                "required": ["message"]
            },
            function=self._run
        )

    def _run(self, message: str) -> str:
        logger.debug(f"Received: {message}")
        
        response = self.agent.run([ChatMessage.from_user(message)])
        message = response["last_message"].text
        
        logger.debug(f"Response: {message}")
        
        return message