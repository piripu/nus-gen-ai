from haystack.components.agents import Agent
from haystack.tools import tool
from haystack.tools.tool import Tool

import logging
from factory import create_chat_generator
from weather_agent import WeatherAgentTool
from events_agent import EventsAgentTool
from document_agent import DocumentAgentTool
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
        DocumentAgentTool()
    ]

SYSTEM_PROMPT = """You are an orchestrator agent that can assist users by leveraging multiple specialized agents to fulfill their requests.
Your task is to help the user plan their itinerary based on the weather forecast and events on a specified location.
Always ensure that the information you provide is accurate and relevant to the user's request.
When you respond, try to include both the weather forecast and a list of events happening in the specified location on the given date.
You may also be asked to answer questions based on user documents.
"""

class OrchestratorAgent(Agent):
    def __init__(self):
        super().__init__(
            chat_generator=create_chat_generator(),
            system_prompt=SYSTEM_PROMPT,
            tools=get_agent_tools(),
        )