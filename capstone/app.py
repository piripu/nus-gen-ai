from datetime import datetime
from haystack.dataclasses import ChatMessage, ChatRole
from haystack_experimental.chat_message_stores.in_memory import InMemoryChatMessageStore
from rich import print

import config, logging, factory, os
from config import load_config
from orchestrator_agent import OrchestratorAgent

load_config()

assistant_chat_color = "green"
user_chat_color = "blue"
system_chat_color = "yellow"

def configure_file_logger():
    logger = logging.getLogger()
    logger.setLevel(config.LOG_LEVEL)
    logging.getLogger("haystack").setLevel(config.LOG_LEVEL)

    fh = logging.FileHandler("debug.log")
    fh.setLevel(config.LOG_LEVEL)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)

    logger.addHandler(fh)

def print_chat_message(message: ChatMessage):
    role = "User" if message.is_from(ChatRole.USER) else "Assistant" if message.is_from(ChatRole.ASSISTANT) else "System"
    color = user_chat_color if message.is_from(ChatRole.USER) else assistant_chat_color if message.is_from(ChatRole.ASSISTANT) else system_chat_color
    print(f"[bold {color}]{role}:[/bold {color}] {message.text}")
    
def save_conversation(chat_store: InMemoryChatMessageStore):
    user_docs = config.USER_DOCS_DIR
    if not os.path.exists(user_docs):
        os.makedirs(user_docs)
    timenow = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(os.path.join(user_docs, f"conversation_log_{timenow}.txt"), "w") as file:
        for message in chat_store.messages:
            role = "User" if message.is_from(ChatRole.USER) else "Assistant" if message.is_from(ChatRole.ASSISTANT) else "System"
            file.write(f"{role}: {message.text}\n")

if __name__ == "__main__":
    configure_file_logger()

    print(f"[bold {assistant_chat_color}]Enter your name to start[/bold {assistant_chat_color}]: ", end="")
    name = input()
    
    chat_store = factory.create_chatmessage_store()
    agent = OrchestratorAgent(name)
    agent_response = agent.greet_user()
    chat_store.write_messages([agent_response])
    print_chat_message(agent_response)

    while True:
        print(f"[bold {user_chat_color}]{name}[/bold {user_chat_color}]: ", end="")
        query = input()
        
        user_message = ChatMessage.from_user(query)
        chat_store.write_messages([user_message])
        
        if query.lower() in ["/exit", "/quit", "/bye"]:
            print(f"[bold {assistant_chat_color}]Exiting the chat. Goodbye![/bold {assistant_chat_color}]")
            break
        
        response = agent.run(chat_store.messages)
        chat_store.write_messages([response["last_message"]])
        print_chat_message(response["last_message"])

    save_conversation(chat_store)