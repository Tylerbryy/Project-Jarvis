import openai
import requests
from PIL import Image
from io import BytesIO
from typing import Tuple
import os
from dotenv import load_dotenv
load_dotenv()


openai.api_key = os.getenv("OPEN_AI_APIKEY")

def generate_image(prompt: str, image_size: Tuple[int, int] = (512, 512)) -> Image:
    response = openai.Image.create(prompt=prompt, n=1, size=f"{image_size[0]}x{image_size[1]}")
    image_url = response['data'][0]['url']

    # Download the image from the URL
    image_data = requests.get(image_url).content

    # Create a Pillow image object from the downloaded data
    image = Image.open(BytesIO(image_data))
    
    return image.show()


