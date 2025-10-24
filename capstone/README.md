# Capstone Project

Author: Esguerra, Phillip Amir

## Usage

- At first run, will download the embedding model from huggingface

## Architecture

### RAG Pipeline

- Use inmemory and discard the file after use
- limited to simple embedding search
- for better context management, it will be ideal to do
  - summarization of chunks
  - add hierarchichal or sliding window summarization function to summarize the whole file

### Decision Records

| Concern | Context | Resolution |
| --- | --- | --- |
| Use of LangChain | Based from previous experience, use of LangChain is very challenging. Community notes varies from version to version and the documentation is difficult to navigate. This might've changed with version 1.0 but there should be other options with better API. | Use Haystack. It has better API and documentation in my opinion. |
| Agent Orchestration | Manually inspecting the response of the orchestrator agent will introduce coupling if more agents is introduced, in terms of adding it to context. | Wrap other agents as a tool to describe their capabilities and let the orchestrator agent decide on which tool to use. |