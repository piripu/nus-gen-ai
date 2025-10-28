from typing import Annotated, Literal
from haystack.components.agents import Agent
from haystack.dataclasses import ChatMessage
from haystack.tools import tool
from haystack.tools.tool import Tool

import helpers.weather as weather
from helpers.factory import create_chat_generator

import logging
logger = logging.getLogger(__name__)

@tool
def get_current_weather(
    location: Annotated[str, "the city for which to get the weather"]):
    '''Get the current weather for a location.'''
    try:
        result = weather.get_current_weather(location)
        logger.debug("Weather fetch result: %s", str(result))

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
            system_prompt="You are a weather information agent. Use the tools available to provide accurate weather data.",
            tools=[get_current_weather])
        
# We create a tool wrapper for the weather agent that only takes a message as input
class WeatherAgentTool(Tool):
    name = "weather_agent_tool"
    description = "A tool that provides weather information based on user queries."

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
                        "description": "Request message to get weather information for a specific location. Date and time may be included when possible."
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