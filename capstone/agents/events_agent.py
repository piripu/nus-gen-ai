from typing import Annotated
from haystack.components.agents import Agent
from haystack.dataclasses import ChatMessage
from haystack.tools import tool
from haystack.tools.tool import Tool

import helpers.database as db
from helpers.factory import create_chat_generator
from helpers import ListJSONEncoder

import logging, json
logger = logging.getLogger(__name__)

@tool
def get_events(
    date: Annotated[str, "the date for which to get the events. Format: YYYY-MM-DD"]):
    '''Get the for list of events for a specific date.'''
    events = db.get_events_by_date(date)
    if not events:
        return json.dumps([])
    return json.dumps(events, cls=ListJSONEncoder)

class EventsAgent(Agent):
    def __init__(self):
        super().__init__(
            chat_generator=create_chat_generator(),
            system_prompt="You are an event information agent. Use the tools available to get list of events for a specific date.",
            tools=[get_events])
        
# We create a tool wrapper for the weather agent that only takes a message as input
class EventsAgentTool(Tool):
    name = "events_agent_tool"
    description = """A tool that provides event information based on user queries. 
    Provide the current date today.
    Provide future dates for events up until 14 days from the current date."""

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
                        "description": "Request message to get event information for a date. Provide the current date today. List of events is only feasible up until 14 days from the current date."
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