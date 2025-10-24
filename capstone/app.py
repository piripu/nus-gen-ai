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

    user_message = ChatMessage.from_user("Using this ./ra 12305-clean.txt file path, can you help me understand the final provisions in Liability and Financial Security in the Event of a Nuclear Accident? Summarize in ELI5.")
    response = agent.run([user_message])
    print(response["last_message"].text)
    
    # from rag_pipeline import run_incontext_pipeline

    # file_path = "./ra 12305-clean.txt"
    # query = "What are the final provisions in Liability and Financial Security in the Event of a Nuclear Accident? Summarize in baby uwu tone."
    # response = run_incontext_pipeline(file_path, query)
    # print(response)
    