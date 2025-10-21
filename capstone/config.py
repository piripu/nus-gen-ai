import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')

LOG_LEVEL = "DEBUG"

OPENAI_MODEL_NAME = "gpt-4"
# OLLAMA_MODEL_NAME = "qwen3:8b"
OLLAMA_MODEL_NAME = "llama3.1:8b-instruct-q8_0"

ENABLE_LOCAL=True

def load_config():
    load_dotenv()