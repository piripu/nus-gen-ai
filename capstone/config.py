import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
SERPERDEV_API_KEY = os.getenv('SERPERDEV_API_KEY')

LOG_LEVEL = "DEBUG"

OPENAI_CHAT_MODEL_NAME = "gpt-4"
OLLAMA_CHAT_MODEL_NAME = "qwen3:8b"
OLLAMA_EMBEDDING_MODEL_NAME = "embeddinggemma"

USER_DOCS_DIR = ".user_docs"

USE_LOCAL_MODEL = True
USE_INMEMORY = True

# Uses an LLM to generate mock weather data instead of calling a real weather API
USE_MOCK_WEATHER = False

CURRENT_USER_DIR = None

def load_config():
    load_dotenv()