#!/usr/bin/env python3
"""
Bibble Setup and Test Script
Run this script to verify your installation and configuration.
"""

import os
import sys
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import aiohttp
        import aiofiles
        import dotenv
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists and has required variables."""
    env_path = Path(".env")
    if not env_path.exists():
        print("❌ .env file not found")
        print("Copy .env.example to .env and configure your Azure OpenAI credentials")
        return False
    
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = [
        "AZURE_SORA_ENDPOINT",
        "AZURE_SORA_API_KEY", 
        "AZURE_IMAGE_ENDPOINT",
        "AZURE_IMAGE_API_KEY"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var) or os.getenv(var) == "EMPTY":
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        return False
    
    print("✅ Environment configuration looks good")
    return True

def check_directories():
    """Check if required directories exist."""
    dirs = ["src", "src/images", "src/scene"]
    for dir_path in dirs:
        if not Path(dir_path).exists():
            print(f"❌ Directory missing: {dir_path}")
            return False
    
    # Create generated directory if it doesn't exist
    generated_dir = Path("src/generated")
    if not generated_dir.exists():
        generated_dir.mkdir(parents=True)
        print("✅ Created src/generated directory")
    
    print("✅ All required directories present")
    return True

def test_imports():
    """Test importing the main modules."""
    try:
        sys.path.insert(0, "src")
        import video
        import design
        print("✅ Bibble modules import successfully")
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    """Run all setup checks."""
    print("🔍 Bibble Setup Check\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Environment Config", check_env_file),
        ("Directories", check_directories),
        ("Module Imports", test_imports)
    ]
    
    all_passed = True
    for name, check_func in checks:
        print(f"Checking {name}...")
        if not check_func():
            all_passed = False
        print()
    
    if all_passed:
        print("🎉 Setup complete! Bibble is ready to use.")
        print("\nNext steps:")
        print("- Run 'python src/video.py' to test video generation")
        print("- Run 'python src/design.py' to test image editing")
    else:
        print("❌ Setup incomplete. Please address the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()