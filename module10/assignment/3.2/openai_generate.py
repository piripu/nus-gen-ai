import base64
from openai import OpenAI
client = OpenAI()

img = client.images.generate(
    model="dall-e-3",
    prompt="a white siamese cat",
    n=1,
    size="1024x1024"
)

image_bytes = base64.b64decode(img.data[0].b64_json)
with open("output.png", "wb") as f:
    f.write(image_bytes)