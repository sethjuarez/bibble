"""
Bibble Video Generation Module

This module provides video generation capabilities using OpenAI's Sora model via Azure OpenAI.
It handles the complete workflow from text description to generated video file, including
job submission, status polling, and file storage.

Dependencies:
    - Azure OpenAI account with Sora model access
    - Environment variables: AZURE_SORA_ENDPOINT, AZURE_SORA_API_KEY

Usage:
    import asyncio
    from video import sora_video_generation
    
    async def main():
        video_path = await sora_video_generation("A peaceful lake scene", seconds=10)
        print(f"Video generated: {video_path}")
    
    asyncio.run(main())
"""

import os
import time
import asyncio
import aiohttp
from pathlib import Path
from dotenv import load_dotenv
from aiohttp.streams import StreamReader

# Load environment variables from .env file
load_dotenv()


BASE_DIR = Path(__file__).resolve().parent

AZURE_SORA_ENDPOINT = os.environ.get("AZURE_SORA_ENDPOINT", "EMPTY").rstrip("/")
AZURE_SORA_API_KEY = os.environ.get("AZURE_SORA_API_KEY", "EMPTY")


async def save_video(stream_reader: StreamReader, filename: str) -> str:
    """
    Save a video stream to the local file system.
    
    Args:
        stream_reader: Async stream reader containing video data
        filename: Name for the output video file (should include .mp4 extension)
        
    Returns:
        str: Full path to the saved video file
        
    The video is saved in the 'generated/' directory relative to this module.
    """
    video_bytes = await stream_reader.read()
    output_path = BASE_DIR / f"generated/{filename}"
    
    # Ensure the generated directory exists
    output_path.parent.mkdir(exist_ok=True)
    
    with open(output_path, "wb") as f:
        f.write(video_bytes)

    return str(output_path)


async def sora_video_generation(description: str, seconds: int = 10) -> str:
    """
    Generate a video using OpenAI's Sora model via Azure OpenAI.
    
    Args:
        description: Text description of the video to generate
        seconds: Duration of the video in seconds (default: 10)
        
    Returns:
        str: Path to the generated video file, or empty string if generation failed
        
    The function creates a video generation job, polls for completion, and downloads
    the result when ready. The video is saved as an MP4 file in the generated/ directory.
    
    Video specifications:
        - Resolution: 1920x1080 (Full HD)
        - Format: MP4
        - Model: Sora
    """

    api_version = "preview"
    create_url = f"{AZURE_SORA_ENDPOINT}/openai/v1/video/generations/jobs?api-version={api_version}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AZURE_SORA_API_KEY}",
    }
    body = {
        "prompt": description,
        "width": 1920,
        "height": 1080,
        "n_seconds": seconds,
        "n_variants": 1,
        "model": "sora",
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(create_url, headers=headers, json=body) as response:
            if response.status != 201:
                error_response = await response.json()
                print(error_response)
                return ""

            response_data = await response.json()
            job_id = response_data["id"]

            status_url = f"{AZURE_SORA_ENDPOINT}/openai/v1/video/generations/jobs/{job_id}?api-version={api_version}"
            status = "started"
            status_data: dict = {}
            while status not in ("succeeded", "failed", "cancelled"):
                # async sleep to avoid hitting the API too frequently
                await asyncio.sleep(5)

                async with session.get(status_url, headers=headers) as status_response:
                    if status_response.status != 200:
                        error_response = await status_response.json()
                        print(error_response)
                        return ""

                    status_data = await status_response.json()
                    if status != status_data["status"]:
                        print(f"Video generation status: {status_data['status']}")

                    status = status_data["status"]

            if status == "succeeded":
                generations = status_data.get("generations", [])
                if generations:
                    generation_id = generations[0].get("id")
                    video_url = f"{AZURE_SORA_ENDPOINT}/openai/v1/video/generations/{generation_id}/content/video?api-version={api_version}"
                    async with session.get(
                        video_url, headers=headers
                    ) as video_response:
                        if video_response.status != 200:
                            error_response = await video_response.json()
                            print(error_response)

                            return ""

                        # Save the video content
                        video_blob = await save_video(video_response.content, f"{job_id}.mp4")
                        return video_blob
    return ""


if __name__ == "__main__":
    import asyncio

    # Example usage
    description = """
    A serene landscape with rolling hills, a clear blue sky, and a gentle stream flowing through the scene. The hills are covered in lush green grass, and wildflowers 
    bloom in various colors. In the distance, there are majestic mountains with snow-capped peaks. The sun is shining brightly, casting soft shadows on the ground. 
    A few fluffy clouds drift lazily across the sky, adding to the peaceful atmosphere.
    """.replace(
        "\n", " "
    ).strip()
    # load all images from the images directory
    

    start_time = time.time()
    result = asyncio.run(sora_video_generation(description, 10))
    end_time = time.time()

    print(f"Result: {result}")
    print(f"Execution time: {end_time - start_time:.2f} seconds")
