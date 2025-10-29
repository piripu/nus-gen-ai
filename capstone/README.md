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
| Use of LangChain | Based from previous experience, use of LangChain is very challenging. Community notes varies from version to version and the documentation is difficult to navigate. This might[...] |
| Agent Orchestration | Manually inspecting the response of the orchestrator agent will introduce coupling if more agents is introduced, in terms of adding it to context. | Wrap other agents as a [...] |

## Technical Details

### Project Structure

- **.assets/**: Contains assets related to the project.
- **.python-version**: Specifies the Python version for the project.
- **README.md**: Includes project documentation.
- **config.py**: Contains configuration settings or parameters.
- **main.py**: The primary script for the project, driving the main functionality.
- **pyproject.toml**: Configuration for Python tools and dependencies.
- **requirements.txt**: Lists project dependencies.
- **uv.lock**: A lock file for dependency management.
- **agents/**: Includes agent-related implementations or modules.
- **helpers/**: Contains helper functions or utilities.

### Agent Structure and Orchestration

- **Agent Structure**: The `agents` directory includes modular agents, each designed for specific tasks. These agents are encapsulated in a way that they can interact with the orchestrator seamlessly.
- **Orchestrator**: The orchestrator acts as a router, delegating tasks to the appropriate agents based on the input context. It centralizes decision-making and manages the flow of information between agents. This architecture ensures scalable and maintainable agent interactions.