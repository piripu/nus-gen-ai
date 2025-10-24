from haystack_integrations.document_stores.chroma import ChromaDocumentStore

import config

def create_chat_generator():
    if config.USE_LOCAL_MODEL:
        from haystack_integrations.components.generators.ollama import OllamaChatGenerator
        return OllamaChatGenerator(model=config.OLLAMA_CHAT_MODEL_NAME)
    else:
        from haystack.components.generators.chat import OpenAIChatGenerator
        # api key is alreadu supplied from environment variable
        return OpenAIChatGenerator(model=config.OPENAI_CHAT_MODEL_NAME)

def create_document_embedder():
    if config.USE_LOCAL_MODEL:
        from haystack_integrations.components.embedders.ollama import OllamaDocumentEmbedder
        return OllamaDocumentEmbedder(model=config.OLLAMA_EMBEDDING_MODEL_NAME)
    else:
        from haystack.components.embedders import OpenAIDocumentEmbedder
        return OpenAIDocumentEmbedder()
    
def create_text_embedder():
    if config.USE_LOCAL_MODEL:
        from haystack_integrations.components.embedders.ollama import OllamaTextEmbedder
        return OllamaTextEmbedder(model=config.OLLAMA_EMBEDDING_MODEL_NAME)
    else:
        from haystack.components.embedders import OpenAITextEmbedder
        return OpenAITextEmbedder()


def create_document_store():
    if config.USE_INMEMORY:
        from haystack.document_stores.in_memory import InMemoryDocumentStore
        return InMemoryDocumentStore()
    else:
        return ChromaDocumentStore(
            persist_path=config.USER_DOCS_DIR)

def create_retriever(**kwargs):
    if config.USE_INMEMORY:
        from haystack.components.retrievers.in_memory import InMemoryEmbeddingRetriever
        return InMemoryEmbeddingRetriever(**kwargs)
    else:
        from haystack_integrations.components.retrievers.chroma import ChromaEmbeddingRetriever
        return ChromaEmbeddingRetriever(**kwargs)
