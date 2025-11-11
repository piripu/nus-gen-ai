import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
VISUAL_CROSSING_API_KEY = os.getenv("VISUAL_CROSSING_API_KEY")
SERPERDEV_API_KEY = os.getenv("SERPERDEV_API_KEY")

LOG_LEVEL = "DEBUG"

OPENAI_CHAT_MODEL_NAME = "gpt-4o-mini"
OPENAI_EMBEDDING_MODEL_NAME = "text-embedding-ada-002"
OLLAMA_CHAT_MODEL_NAME = "qwen3:8b"
OLLAMA_EMBEDDING_MODEL_NAME = "embeddinggemma"

USER_DOCS_DIR = ".user_docs"

USE_LOCAL_MODEL = True
USE_INMEMORY = True

CURRENT_USER_DIR = None

def load_config():
    load_dotenv()

import logging
from haystack import tracing
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.sdk.resources import Resource

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.semconv.attributes.service_attributes import SERVICE_NAME

def configure_logging():
    # Set up OpenTelemetry logging
    resource = Resource(attributes={
        SERVICE_NAME: "capstone-app"
    })

    logger_provider = LoggerProvider(resource=resource)
    log_exporter = OTLPLogExporter(endpoint="http://localhost:18890/v1/logs")
    log_processor = BatchLogRecordProcessor(log_exporter)
    logger_provider.add_log_record_processor(log_processor)

    logging_handler = LoggingHandler(level=logging.DEBUG, logger_provider=logger_provider)
    logging.basicConfig(level=logging.DEBUG, handlers=[logging_handler])
    pass
    
def configure_tracing():
    
    # Service name is required for most backends
    resource = Resource(attributes={
        SERVICE_NAME: "capstone-app"  # Correct constant
    })
    
    tracer_provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://localhost:18890/v1/traces"))
    tracer_provider.add_span_processor(processor)
    trace.set_tracer_provider(tracer_provider)
    
    # Tell Haystack to auto-detect the configured tracer
    import haystack.tracing
    haystack.tracing.auto_enable_tracing()
    
    # Explicitly tell Haystack to use your tracer
    from haystack.tracing import OpenTelemetryTracer
    
    tracer = tracer_provider.get_tracer("capstone-app-tracer")
    tracing.enable_tracing(OpenTelemetryTracer(tracer))
    
    from opentelemetry.instrumentation.urllib3 import URLLib3Instrumentor
    URLLib3Instrumentor().instrument()

    tracing.tracer.is_content_tracing_enabled = True