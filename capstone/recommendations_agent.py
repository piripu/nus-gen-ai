from typing import Annotated
from haystack.components.agents import Agent
from haystack.dataclasses import ChatMessage
from haystack.tools import tool
from haystack.tools.tool import Tool

from factory import create_chat_generator

import logging
logger = logging.getLogger(__name__)

@tool
def search_web(
    query: Annotated[str, "query to search the web"]):
    '''A simple function to search the web. Use this tool to look for events and recommendations using the web..'''
    return f"Search results for '{query}': ..."

class EventsAgent(Agent):
    def __init__(self):
        super().__init__(
            chat_generator=create_chat_generator(),
            # system_prompt="You are a weather information agent. Use the tools available to provide accurate weather data.",
            system_prompt="You are an event information agent. This is for debug for now, just return a realistic event for a given location",
            tools=[get_event])
        
# We create a tool wrapper for the weather agent that only takes a message as input
class EventsAgentTool(Tool):
    name = "events_agent_tool"
    description = "A tool that provides event information based on user queries."

    def __init__(self):
        self.agent = EventsAgent()
        
        super().__init__(
            name=self.name,
            description=self.description,
            parameters = {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Request message to get event information for a specific location. Date and time may be included when possible."
                    }
                },
                "required": ["message"]
            },
            function=self._run
            # function=lambda args: print(args)
        )

    def _run(self, message: str) -> str:
        logger.debug(f"Received: {message}")
        
        response = self.agent.run([ChatMessage.from_user(message)])
        message = response["last_message"].text

        logger.debug(f"Response: {message}")
        
        return message