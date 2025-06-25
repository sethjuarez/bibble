"""
Bibble Image Design and Editing Module

This module provides AI-powered image editing and enhancement capabilities using
Azure OpenAI's image models. It supports both inspiration-based editing and 
precise masked editing workflows.

Features:
    - Single image and batch image processing
    - Mask-based targeted editing
    - Base64 image handling
    - Automatic file management

Dependencies:
    - Azure OpenAI account with image editing model access
    - Environment variables: AZURE_IMAGE_ENDPOINT, AZURE_IMAGE_API_KEY

Usage:
    import asyncio
    import base64
    from design import generate_edit_image
    
    async def main():
        with open("image.jpg", "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")
        
        result = await generate_edit_image("Make it futuristic", image_data)
        print(f"Edited image: {result}")
    
    asyncio.run(main())
"""

import io
import os
import uuid
import time
import base64
import aiohttp
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


BASE_DIR = Path(__file__).resolve().parent

AZURE_IMAGE_ENDPOINT = os.environ.get("AZURE_IMAGE_ENDPOINT", "EMPTY").rstrip("/")
AZURE_IMAGE_API_KEY = os.environ.get("AZURE_IMAGE_API_KEY", "EMPTY")


async def save_image(image_base64: str, filename: str) -> None:
    """
    Save a base64 encoded image to a file.
    
    Args:
        image_base64: Base64 encoded image data
        filename: Name for the output image file (should include extension)
        
    The image is saved in the 'generated/' directory relative to this module.
    """
    image_bytes = base64.b64decode(image_base64)
    output_path = BASE_DIR / f"generated/{filename}"
    
    # Ensure the generated directory exists
    output_path.parent.mkdir(exist_ok=True)
    
    with open(output_path, "wb") as f:
        f.write(image_bytes)


async def generate_edit_image(description: str, image: str | list[str], mask: str | None = None) -> str:
    """
    Generate or edit an image using AI based on a text description.
    
    Args:
        description: Text prompt describing the desired image transformation
        image: Base64 encoded image data (single image or list of images)
        mask: Optional base64 encoded mask for targeted editing
        
    Returns:
        str: Filename of the generated image (stored in generated/ directory)
        
    Raises:
        Exception: If the API request fails or returns an error
        
    This function supports both single image editing and batch processing.
    When a mask is provided, only the masked areas are modified.
    
    Image specifications:
        - Output size: 1024x1024
        - Quality: High
        - Format: PNG
    """
    api_version = "2025-04-01-preview"
    deployment_name = "gpt-image-1"
    endpoint = f"{AZURE_IMAGE_ENDPOINT}/openai/deployments/{deployment_name}/images/edits?api-version={api_version}"
    size: str = "1024x1024"
    quality: str = "high"

    async with aiohttp.ClientSession() as session:
        headers = {
            "api-key": AZURE_IMAGE_API_KEY,
        }

        form_data = aiohttp.FormData()

    
        if isinstance(image, list):
            for i, img_data in enumerate(image):
                img = io.BytesIO(base64.b64decode(img_data))
                form_data.add_field(
                    f"image[{i}]",
                    img,
                    filename=f"image_{i}.png",
                    content_type="image/png",
                )
        else:
            img = io.BytesIO(base64.b64decode(image))
            form_data.add_field(
                "image", img, filename="image.png", content_type="image/png"
            )

        form_data.add_field("prompt", description, content_type="text/plain")
        form_data.add_field("size", size, content_type="text/plain")
        form_data.add_field("quality", quality, content_type="text/plain")
        if mask:
            mask_data = io.BytesIO(base64.b64decode(mask))
            form_data.add_field(
                "mask", mask_data, filename="mask.png", content_type="image/png"
            )

        async with session.post(endpoint, headers=headers, data=form_data) as response:
            if response.status == 200:
                result = await response.json()
                if result and "data" in result and len(result["data"]) > 0:
                    image_base64 = result["data"][0]["b64_json"]
                    image_name = f"{str(uuid.uuid4())}.png"
                    await save_image(image_base64, image_name)
                    return image_name
            else:
                error_message = await response.text()
                raise Exception(f"Error generating image: {error_message}")


async def image_edit_inspiration():
    """
    Example function demonstrating inspiration-based image editing.
    
    This function loads all images from the images/ directory and applies
    a creative transformation based on the provided description. It showcases
    batch processing capabilities for multiple source images.
    """
    # Example usage
    description = """
    Create a futuristic Santa Monica cityscape at night, with neon lights reflecting off wet streets,
    showcasing a blend of modern architecture and classic elements. The scene should be vibrant and bustling,
    with people walking, futuristic vehicles, and a clear night sky filled with stars.
    The atmosphere should evoke a sense of wonder and excitement, capturing the essence of a city that
    never sleeps, blending the charm of Santa Monica with a futuristic twist.
    The image should be rich in detail, with a focus on the interplay of light and shadow
    to create a dynamic and immersive California environment.
    """.replace(
        "\n", " "
    ).strip()
    # load all images from the images directory
    image = [
        base64.b64encode(open(f"{BASE_DIR}/images/{img}", "rb").read()).decode("utf-8")
        for img in os.listdir(f"{BASE_DIR}/images")
        if not img.startswith("_")
    ]

    start_time = time.time()
    result = await generate_edit_image(description, image)
    end_time = time.time()

    print(f"Result: {result}")
    print(f"Execution time: {end_time - start_time:.2f} seconds")


async def image_edit_with_mask():
    """
    Example function demonstrating mask-based image editing.
    
    This function shows how to use masks for precise, targeted image editing.
    It loads a scene image and its corresponding mask, then applies changes
    only to the masked areas while preserving the rest of the image.
    """
    # Example usage
    description = """
    A contemplative person in a serene setting, surrounded by nature contemplating the mysteries of the universe.
    """.replace(
        "\n", " "
    ).strip()
    # load all images from the images directory

    scene = base64.b64encode(open(f"{BASE_DIR}/scene/scene.png", "rb").read()).decode(
        "utf-8"
    )

    mask = base64.b64encode(
        open(f"{BASE_DIR}/scene/_scene_mask.png", "rb").read()
    ).decode("utf-8")

    start_time = time.time()
    result = await generate_edit_image(description, scene, mask=mask)
    end_time = time.time()

    print(f"Result: {result}")
    print(f"Execution time: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    import asyncio

    #asyncio.run(image_edit_inspiration())
    asyncio.run(image_edit_with_mask())
