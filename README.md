# Bibble - AI-Powered Creative Content Generation

Bibble is a powerful Python toolkit for generating and editing multimedia content using Azure OpenAI services. It provides seamless integration with OpenAI's cutting-edge models including Sora for video generation and DALL-E for image editing and enhancement.

## ✨ Features

- **🎬 Video Generation**: Create stunning videos from text descriptions using OpenAI's Sora model
- **🎨 Image Editing**: Edit and enhance images with AI-powered tools
- **🎭 Masked Editing**: Precise image editing using custom masks for targeted modifications  
- **📁 Batch Processing**: Handle multiple images and complex editing workflows
- **⚡ Async Operations**: High-performance asynchronous processing for efficient content generation
- **🔧 Easy Configuration**: Simple environment-based configuration management

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Azure OpenAI account with access to:
  - Sora model for video generation
  - Image generation/editing models (DALL-E)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sethjuarez/bibble.git
   cd bibble
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```env
   # Azure OpenAI Sora Configuration
   AZURE_SORA_ENDPOINT=https://your-sora-endpoint.openai.azure.com
   AZURE_SORA_API_KEY=your-sora-api-key

   # Azure OpenAI Image Configuration  
   AZURE_IMAGE_ENDPOINT=https://your-image-endpoint.openai.azure.com
   AZURE_IMAGE_API_KEY=your-image-api-key
   ```

## 📖 Core Components

### 🎬 Video Generation (`src/video.py`)

The video generation module leverages OpenAI's Sora model to create high-quality videos from text descriptions.

#### Key Functions:

- **`sora_video_generation(description: str, seconds: int = 10) -> str`**
  - Generates a video based on the provided text description
  - Returns the path to the generated video file
  - Supports customizable video duration (default: 10 seconds)

- **`save_video(stream_reader: StreamReader, filename: str) -> str`**
  - Saves video content from API response to local storage
  - Automatically manages file creation in the `generated/` directory

#### How it Works:

1. **Job Creation**: Submits a video generation request to Azure Sora API
2. **Status Polling**: Monitors job completion with intelligent polling intervals
3. **Content Retrieval**: Downloads the generated video when ready
4. **Local Storage**: Saves the video file for immediate use

#### Configuration:
- **Resolution**: 1920x1080 (Full HD)
- **Format**: MP4
- **Model**: Sora
- **Output Location**: `src/generated/`

#### Example Usage:
```python
import asyncio
from src.video import sora_video_generation

async def create_video():
    description = """
    A serene landscape with rolling hills, a clear blue sky, and a gentle stream 
    flowing through the scene. The hills are covered in lush green grass, and 
    wildflowers bloom in various colors.
    """
    
    video_path = await sora_video_generation(description, seconds=15)
    print(f"Video created at: {video_path}")

# Run the example
asyncio.run(create_video())
```

### 🎨 Image Editing (`src/design.py`)

The image editing module provides powerful AI-driven image manipulation capabilities using Azure OpenAI's image models.

#### Key Functions:

- **`generate_edit_image(description: str, image: str | list[str], mask: str | None = None) -> str`**
  - Main function for AI-powered image editing
  - Supports single images or batch processing of multiple images
  - Optional mask support for precise, targeted editing
  - Returns the filename of the generated image

- **`save_image(image_base64: str, filename: str) -> None`**
  - Converts base64 image data to local files
  - Manages storage in the `generated/` directory

- **`image_edit_inspiration() -> None`**
  - Example workflow for inspiration-based editing
  - Processes all images from the `images/` directory
  - Demonstrates batch image processing capabilities

- **`image_edit_with_mask() -> None`**
  - Example workflow for mask-based precision editing
  - Uses scene images with custom masks for targeted modifications

#### Supported Workflows:

1. **Inspiration Editing**: Transform existing images based on creative prompts
2. **Masked Editing**: Precise modifications using custom masks
3. **Batch Processing**: Handle multiple images simultaneously
4. **Style Transfer**: Apply artistic styles and transformations

#### Configuration:
- **Resolution**: 1024x1024
- **Quality**: High
- **Format**: PNG
- **API Version**: 2025-04-01-preview
- **Deployment**: gpt-image-1

#### Example Usage:

**Basic Image Editing:**
```python
import asyncio
import base64
from src.design import generate_edit_image

async def edit_image():
    # Load and encode image
    with open("my_image.jpg", "rb") as f:
        image_data = base64.b64encode(f.read()).decode("utf-8")
    
    description = "Transform this into a futuristic cyberpunk scene with neon lights"
    result = await generate_edit_image(description, image_data)
    print(f"Edited image saved as: {result}")

asyncio.run(edit_image())
```

**Masked Editing:**
```python
async def masked_edit():
    # Load base image and mask
    with open("scene.png", "rb") as f:
        scene_data = base64.b64encode(f.read()).decode("utf-8")
    
    with open("mask.png", "rb") as f:
        mask_data = base64.b64encode(f.read()).decode("utf-8")
    
    description = "A beautiful sunset sky"
    result = await generate_edit_image(description, scene_data, mask=mask_data)
    print(f"Masked edit completed: {result}")

asyncio.run(masked_edit())
```

## 📁 Project Structure

```
bibble/
├── src/                          # Source code directory
│   ├── video.py                  # Video generation module
│   ├── design.py                 # Image editing module
│   ├── images/                   # Source images for editing
│   │   ├── Santa_Monica_Downtown.jpg
│   │   └── pier.jpg
│   ├── scene/                    # Scene images and masks
│   │   ├── scene.png             # Base scene image
│   │   └── _scene_mask.png       # Mask for targeted editing
│   └── generated/                # Output directory (auto-created)
├── requirements.txt              # Python dependencies
├── .env                         # Environment configuration (create this)
├── .gitignore                   # Git ignore rules
├── LICENSE                      # MIT License
└── README.md                    # This documentation
```

## 🛠️ Development

### Dependencies

The project uses the following key dependencies:

- **`aiohttp`**: Asynchronous HTTP client for API communications
- **`aiofiles`**: Asynchronous file operations
- **`python-dotenv`**: Environment variable management
- **`types-aiofiles`**: Type hints for aiofiles

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `AZURE_SORA_ENDPOINT` | Azure OpenAI Sora service endpoint | Yes (for video) |
| `AZURE_SORA_API_KEY` | API key for Sora service | Yes (for video) |
| `AZURE_IMAGE_ENDPOINT` | Azure OpenAI Image service endpoint | Yes (for images) |
| `AZURE_IMAGE_API_KEY` | API key for Image service | Yes (for images) |

### Running Examples

**Video Generation:**
```bash
cd src
python video.py
```

**Image Editing:**
```bash
cd src
python design.py
```

### API Rate Limits

- The video generation includes intelligent polling with 5-second intervals
- Image editing processes are optimized for batch operations
- All operations use async/await for non-blocking execution

## 🔧 Configuration Guide

### Azure OpenAI Setup

1. **Create Azure OpenAI Resource**:
   - Navigate to Azure Portal
   - Create a new OpenAI resource
   - Note the endpoint URL and API key

2. **Deploy Models**:
   - Deploy Sora model for video generation
   - Deploy image editing model (DALL-E)
   - Note deployment names and API versions

3. **Configure Access**:
   - Ensure your Azure subscription has access to preview features
   - Configure appropriate role-based access control (RBAC)

### File Organization

- **Input Images**: Place source images in `src/images/`
- **Scene Assets**: Store scene files and masks in `src/scene/`
- **Generated Content**: Output automatically saved to `src/generated/`

## 🐛 Troubleshooting

### Common Issues

1. **API Authentication Errors**:
   - Verify your API keys and endpoints in `.env`
   - Check Azure OpenAI resource permissions
   - Ensure model deployments are active

2. **File Not Found Errors**:
   - Verify image paths in `src/images/` and `src/scene/`
   - Ensure `generated/` directory exists (created automatically)

3. **Video Generation Timeouts**:
   - Video generation can take several minutes
   - Monitor console output for status updates
   - Check Azure OpenAI service quotas

4. **Image Processing Failures**:
   - Verify image formats (PNG/JPG supported)
   - Check file size limitations
   - Ensure base64 encoding is correct

### Debug Mode

Enable verbose logging by modifying the print statements in the source files or add Python logging configuration for detailed troubleshooting.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📞 Support

For questions, issues, or feature requests, please create an issue in the GitHub repository.

---

**Built with ❤️ by Seth Juarez**

*Bibble empowers creators with AI-driven content generation, making professional-quality video and image creation accessible to everyone.*