from haystack.dataclasses import ChatMessage, ChatRole
from haystack_experimental.chat_message_stores.in_memory import InMemoryChatMessageStore
from datetime import datetime

import config, os

def get_user_conversation_dir() -> str:

    if config.CURRENT_USER_DIR is not None:
        return config.CURRENT_USER_DIR

    user_docs = config.USER_DOCS_DIR
    if not os.path.exists(user_docs):
        os.makedirs(user_docs)
        
    timenow = datetime.now().strftime("%y%m%d%H%M%S")
    user_dir = os.path.join(user_docs, f"{timenow}")
    os.makedirs(user_dir)

    config.CURRENT_USER_DIR = user_dir
    
    return user_dir

def save_conversation(user_dir: str, chat_store: InMemoryChatMessageStore):
    with open(os.path.join(user_dir, f"conversation_log.txt"), "w") as file:
        for message in chat_store.messages:
            role = "User" if message.is_from(ChatRole.USER) else "Assistant" if message.is_from(ChatRole.ASSISTANT) else "System"
            file.write(f"{role}: {message.text}\n")
