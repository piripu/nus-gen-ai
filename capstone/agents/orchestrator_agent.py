from haystack.components.agents import Agent
from haystack.dataclasses import ChatMessage
from haystack.tools import tool
from haystack.tools.tool import Tool

import logging
from factory import create_chat_generator
from agents.weather_agent import WeatherAgentTool
from agents.events_agent import EventsAgentTool
from agents.document_agent import DocumentAgentTool
from agents.image_generation_agent import ImageGenerationAgentTool
from agents.recommendations_agent import RecommendationsAgentTool
# orchestrator states
# date: str, time:str, location:str, weather:str, calendar_events:list[str]

logger = logging.getLogger(__name__)

@tool
def get_current_date():
    '''A simple function to get the current date.'''
    from datetime import datetime
    logger.debug("Getting current date")
    current_datetime = datetime.now().strftime("%Y-%m-%d")
    logger.debug(f"Current date is: {current_datetime}")
    return current_datetime

def get_agent_tools() -> list[Tool]:
    return [
        get_current_date,
        WeatherAgentTool(),
        EventsAgentTool(),
        DocumentAgentTool(),
        ImageGenerationAgentTool(),
        RecommendationsAgentTool()
    ]

SYSTEM_PROMPT = """You are an orchestrator agent that will assist <name_of_user>{name}</name_of_user> by leveraging multiple specialized agents to fulfill their requests.
You may have the following tasks, provide weather forecasts, suggest events happening in a location, generate images based on prompts,
and answer questions based on user documents. Always ensure that the information you provide is accurate and relevant to the user's request.
When you respond, be concise and to the point and try to include the name of the user in your responses if only possible.
"""

class OrchestratorAgent(Agent):
    def __init__(self, user_name: str):
        self.user_name = user_name
        super().__init__(
            chat_generator=create_chat_generator(),
            system_prompt=SYSTEM_PROMPT.format(name=user_name),
            tools=get_agent_tools(),
        )
    
    def greet_user(self) -> ChatMessage:
        message = [ChatMessage.from_system(f"Greet the user '{self.user_name}' warmly and introduce yourself as their personal assistant.")]
        response = self.chat_generator.run(message)
        response_text = response["replies"][-1].text
        return ChatMessage.from_assistant(response_text)