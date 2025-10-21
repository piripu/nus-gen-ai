from haystack.dataclasses import Document, ChatMessage
import config, logging
from config import load_config
from weather_agent import WeatherAgent, WeatherAgentTool
from events_agent import EventsAgent, EventsAgentTool
from orchestrator_agent import OrchestratorAgent

load_config()

def configure_file_logger():
    logger = logging.getLogger()
    logger.setLevel(config.LOG_LEVEL)
    logging.getLogger("haystack").setLevel(config.LOG_LEVEL)

    fh = logging.FileHandler("debug.log")
    fh.setLevel(config.LOG_LEVEL)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    logger.addHandler(fh)

if __name__ == "__main__":
    configure_file_logger()
    
    # weather_tool = WeatherAgentTool()
    # events_tool = EventsAgentTool()

    # print(weather_tool.invoke(message="What's the weather like in New York City today?"))
    # print(events_tool.invoke(message="List of events happening in Manila, Philippines on October 23"))

    agent = OrchestratorAgent()

    user_message = ChatMessage.from_user("Plan my itinerary in Manila on October 23?")
    response = agent.run([user_message])
    print(response["last_message"].text)