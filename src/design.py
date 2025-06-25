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


async def save_image(image_base64: str, filename: str):
    """
    Save a base64 encoded image to a file.
    """
    image_bytes = base64.b64decode(image_base64)
    with open(BASE_DIR / f"generated/{filename}", "wb") as f:
        f.write(image_bytes)


async def generate_edit_image(description: str, image: str | list[str], mask: str | None = None):
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
