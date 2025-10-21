from haystack.dataclasses import Document, ChatMessage
import config, logging
from config import load_config
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
    
    agent = OrchestratorAgent()

    user_message = ChatMessage.from_user("Plan my itinerary in Manila on October 23?")
    response = agent.run([user_message])
    print(response["last_message"].text)