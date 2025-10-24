from haystack import Document
from haystack.components.agents import Agent
from haystack.components.converters import PyPDFToDocument, TextFileToDocument, MarkdownToDocument
from haystack.components.joiners import DocumentJoiner
from haystack.components.preprocessors import DocumentCleaner
from haystack.components.preprocessors import DocumentSplitter
from haystack.components.routers import FileTypeRouter
from haystack.components.writers import DocumentWriter
from haystack.document_stores.types import DuplicatePolicy
from haystack.core.pipeline import Pipeline
from haystack.dataclasses import ChatMessage
from haystack.tools import tool
from haystack.tools.tool import Tool
from haystack_integrations.document_stores.chroma import ChromaDocumentStore
from typing import Annotated

import config, logging, os
from factory import create_chat_generator
from rag_pipeline import create_ingestion_pipeline, create_retrieval_pipeline

logger = logging.getLogger(__name__)

# Ensure that user_docs directory exists
user_docs = config.USER_DOCS_DIR
if not os.path.exists(user_docs):
    os.makedirs(user_docs)


@tool
def store_user_document(
  file_path: Annotated[str, "the file path to store the user document"]):
  '''stores the user document in the vector database'''
  document = Document.from_file(file_path)
  
  ingestion_pipeline = create_ingestion_pipeline()
  
  ingestion_pipeline.run({
      "file_router":{
          "sources": [file_path]
      }
  })
  
  return f"User document stored at {file_path}"