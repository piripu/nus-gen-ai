# Capstone Project

Author: Esguerra, Phillip Amir

## Project Initialization

To initialize the project, follow the steps below:

### Using `uv` (Preferred Method)

1. Ensure you have `uv` installed. If not, install it using pip:

   ```bash
   pip install uv
   ```

2. Activate the virtual environment (if created):

   ```bash
   source venv/bin/activate  # On Windows, use `venv\\Scripts\\activate`
   ```

3. Restore the project environment using `uv`:

   ```bash
   uv restore
   ```

### Using `requirements.txt` (Alternative Method)

1. Ensure you have Python installed on your system.

2. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\\Scripts\\activate`
   ```

3. Activate the virtual environment:

   ```bash
   source venv/bin/activate  # On Windows, use `venv\\Scripts\\activate`
   ```

4. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The project configuration is designed to be simple and flexible. Below are the details of the configuration setup:

### `.env` File

- The `.env` file contains sensitive API keys required for the project to function. This file will be included in the project submission but the API keys will be deleted days after grading.
- Checkers can provide their own API keys by updating the `.env` file.

### Default Configuration

- The project is configured to use cloud-based models instead of local models.
- By default, any documents uploaded during a session will be stored in memory and discarded after the console session ends.

### **No Further Changes Needed in Configuration**

- Once the project is sent, no changes are required in the configuration. The setup is ready to use as is.

## Usage

To run the application, follow these steps:

1. Navigate to the project directory in your terminal.

2. Activate the virtual environment (if created):

   ```bash
   source venv/bin/activate  # On Windows, use `venv\\Scripts\\activate`
   ```

3. Run the application using the following command:

   ```bash
   python main.py
   ```

4. At first prompt, provide your name for a better user experience.

5. To terminate the chat session, you can use any of the following commands:
   - `/bye`
   - `/exit`
   - `/quit`

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