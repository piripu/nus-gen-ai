from haystack_integrations.components.generators.ollama import OllamaChatGenerator
from haystack.components.generators.chat import OpenAIChatGenerator

import config

def create_chat_generator():
    if config.ENABLE_LOCAL:
        return OllamaChatGenerator(model=config.OLLAMA_MODEL_NAME)
    else:
        # api key is alreadu supplied from environment variable
        return OpenAIChatGenerator(model=config.OPENAI_MODEL_NAME)