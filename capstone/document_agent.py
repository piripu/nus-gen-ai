from haystack.components.agents import Agent
from haystack.dataclasses import ChatMessage
from haystack.tools import tool
from haystack.tools.tool import Tool
from typing import Annotated

import config, logging, os
from factory import create_chat_generator
from rag_pipeline import create_document_store, create_ingestion_pipeline, create_query_pipeline

logger = logging.getLogger(__name__)

# Ensure that user_docs directory exists
user_docs = config.USER_DOCS_DIR
if not os.path.exists(user_docs):
    os.makedirs(user_docs)

def run_incontext_pipeline(file_path: str, query: str) -> str:
    document_store = create_document_store()
    ingestion_pipeline = create_ingestion_pipeline(document_store)
    
    ingestion_pipeline.run({
        "file_router": {
            "sources": [file_path]
        }
    })

    query_pipeline = create_query_pipeline(document_store=document_store)
    response = query_pipeline.run({
        "embedder": { "text": query },
        "prompt_builder": { "query": query }
    })
    
    return response["llm"]["replies"][-1].text

@tool
def query_document(
    file_path: Annotated[str, "the file path of the document to query"],
    query: Annotated[str, "the query to ask about the document"]):
    '''queries the user document in the vector database'''
    
    response = run_incontext_pipeline(file_path, query)

    return response

class DocumentAgent(Agent):
    def __init__(self):
        super().__init__(
            chat_generator=create_chat_generator(),
            system_prompt="""You are a document question answering agent.
            Use the tools available to provide accurate answers based on the provided document.""",
            tools=[query_document])
        
class DocumentAgentTool(Tool):
    name = "document_agent_tool"
    description = """A tool that provides document information based on provided file path and user queries.
    Use this tool especially if the user provided a file path."""

    def __init__(self):
        self.agent = DocumentAgent()
        
        super().__init__(
            name=self.name,
            description=self.description,
            parameters = {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Request message to get document information for with the provided file path."
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