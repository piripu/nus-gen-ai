from haystack.components.builders import ChatPromptBuilder
from haystack.components.converters import PyPDFToDocument, TextFileToDocument, MarkdownToDocument
from haystack.components.joiners import DocumentJoiner
from haystack.components.preprocessors import DocumentCleaner
from haystack.components.preprocessors import DocumentSplitter
from haystack.components.routers import FileTypeRouter
from haystack.components.writers import DocumentWriter
from haystack.core.pipeline import Pipeline
from haystack.dataclasses import ChatMessage
from haystack.document_stores.in_memory import InMemoryDocumentStore

import factory

prompt = """
Answer the query based on the provided context.
If the context does not contain the answer, say 'Answer not found'.
Context:
{% for doc in documents %}
  {{ doc.content }}
{% endfor %}
query: {{query}}
Answer:
"""

def create_document_store():
    return InMemoryDocumentStore()

def attach_doc_cleaner_and_splitter(
    pipeline: Pipeline,
    document_converter,
    router: str,
    section_name: str,
    doc_splitter_name: str = "document_splitter"
):
    converter_component_name = f"{section_name}_to_doc"
    cleaner_component_name = f"{section_name}_cleaner"
    splitter_component_name = f"{section_name}_splitter"

    pipeline.add_component(converter_component_name, document_converter)
    pipeline.add_component(cleaner_component_name, DocumentCleaner())
    pipeline.add_component(splitter_component_name, DocumentSplitter())

    pipeline.connect(router, f"{converter_component_name}.sources")
    pipeline.connect(converter_component_name, cleaner_component_name)
    pipeline.connect(cleaner_component_name, splitter_component_name)
    pipeline.connect(f"{splitter_component_name}.documents", f"{doc_splitter_name}.documents")
    
    pass

def create_ingestion_pipeline(document_store, pipeline: Pipeline = Pipeline(), print_pipeline: bool = True) -> Pipeline:
    file_router = FileTypeRouter(
        mime_types=[
            "text/plain",
            "text/markdown",
            "application/pdf"
        ])
    pipeline.add_component("file_router", file_router)
    pipeline.add_component("document_joiner", DocumentJoiner())
    attach_doc_cleaner_and_splitter(pipeline, TextFileToDocument(), "file_router.text/plain", "text", "document_joiner")
    attach_doc_cleaner_and_splitter(pipeline, MarkdownToDocument(), "file_router.text/markdown", "md", "document_joiner")
    attach_doc_cleaner_and_splitter(pipeline, PyPDFToDocument(), "file_router.application/pdf", "pdf", "document_joiner")
    # attach_doc_cleaner_and_splitter(pipeline, TextFileToDocument(), "file_router.text/csv", "csv", "document_joiner")

    document_embedder = factory.create_document_embedder()
    pipeline.add_component("embedder", document_embedder)
    
    document_writer = DocumentWriter(document_store)
    pipeline.add_component("writer", document_writer)

    pipeline.connect("document_joiner.documents", "embedder.documents")
    pipeline.connect("embedder.documents", "writer.documents")

    if print_pipeline:
        pipeline.draw(path=r"./.assets/ingestion_pipeline.png")

    return pipeline

def create_query_pipeline(document_store, pipeline: Pipeline = Pipeline(), print_pipeline: bool = True) -> Pipeline:
    embedder = factory.create_text_embedder()
    pipeline.add_component("embedder", embedder)
    
    retriever = factory.create_retriever(document_store=document_store)
    pipeline.add_component("retriever", retriever)
    
    template = [ChatMessage.from_user(prompt)]
    pipeline.add_component("prompt_builder", ChatPromptBuilder(template=template))

    pipeline.add_component("llm", factory.create_chat_generator())

    pipeline.connect("embedder", "retriever.query_embedding")
    pipeline.connect("retriever.documents", "prompt_builder.documents")
    pipeline.connect("prompt_builder", "llm")

    if print_pipeline:
        pipeline.draw(path=r"./.assets/query_pipeline.png")

    return pipeline
