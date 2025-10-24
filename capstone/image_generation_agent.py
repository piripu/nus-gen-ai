from typing import Annotated
from haystack.components.agents import Agent
from haystack.dataclasses import ChatMessage
from haystack.tools import tool
from haystack.tools.tool import Tool
from haystack.components.generators import DALLEImageGenerator

from factory import create_chat_generator

import logging, base64, os, config
logger = logging.getLogger(__name__)

@tool
def generate_image(
    prompt: Annotated[str, "the prompt for the image generation"]):
    '''Function to generate an image based on the prompt and provide the file path of the generated image.'''

    image_generator = DALLEImageGenerator(
        response_format="b64_json"
    )
    image_generator.warm_up()
    response = image_generator.run(prompt)
    image_bytes = base64.b64decode(response["images"][0])
    output_image_path = os.path.join(config.USER_DOCS_DIR, "output.png")
    
    with open(output_image_path, "wb") as f:
        f.write(image_bytes)

    return output_image_path

class ImageGenerationAgent(Agent):
    def __init__(self):
        super().__init__(
            chat_generator=create_chat_generator(),
            system_prompt="""You are an image generation agent.
            Use the tools available to generate images based on user prompts and provide the file path of the generated image back to the user.
            Once the tool provided the image path, respond with the image path only and tell the user that the image has been generated.
            Do not reply in markdown format.""",
            tools=[generate_image])
        
class ImageGenerationAgentTool(Tool):
    name = "image_generation_agent_tool"
    description = """A tool that generates images based on user prompts.
    Once the tool provides the image path, respond with the image path only and tell the user that the image has been generated.
    Do not reply in markdown format."""

    def __init__(self):
        self.agent = ImageGenerationAgent()
        
        super().__init__(
            name=self.name,
            description=self.description,
            parameters = {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Request message to generate an image based on the user's prompt."
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