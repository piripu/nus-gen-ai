from typing import Annotated
from haystack.components.agents import Agent
from haystack.dataclasses import ChatMessage
from haystack.tools import tool
from haystack.tools.tool import Tool

from helpers.factory import create_chat_generator

import logging
logger = logging.getLogger(__name__)

@tool
def search_web(
    query: Annotated[str, "query to search the web"]):
    '''A simple function to search the web. Use this tool to look for events, itinerary and recommendations using the web..'''
    return f"Search results for '{query}': ..."

class RecommendationsAgent(Agent):
    def __init__(self):
        super().__init__(
            chat_generator=create_chat_generator(),
            system_prompt="""You are a itinerary recommendations agent.
            Use the web search tool to provide more accurate itinerary recommendations based on user needs.""",
            tools=[search_web])
        
class RecommendationsAgentTool(Tool):
    name = "recommendations_agent_tool"
    description = "A tool that uses web search to provides event, itinerary and travel information based on user queries."

    def __init__(self):
        self.agent = RecommendationsAgent()

        super().__init__(
            name=self.name,
            description=self.description,
            parameters = {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Request message to get event, itinerary and travel information for a specific location. Date and time may be included when possible."
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