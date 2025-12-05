#!/usr/bin/env python3
"""
Script to start the llm-core server locally.
"""

import os
import subprocess
import sys
from pathlib import Path

def install_dependencies():
    """Install dependencies if needed."""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        sys.exit(1)

def load_env():
    """Load environment variables."""
    env_file = Path(".env")
    if env_file.exists():
        print("📋 .env file found and loaded")
        return True
    else:
        print("⚠️  .env file not found, using default values")
        return False

def start_server():
    """Start the uvicorn server."""
    # Load configurations from environment
    host = os.getenv("HOST", "127.0.0.1")
    port = os.getenv("PORT", "8001")
    log_level = os.getenv("LOG_LEVEL", "info")
    reload = os.getenv("DEBUG", "true").lower() == "true"
    
    print(f"🚀 Starting server on http://{host}:{port}")
    print(f"📄 API documentation available at http://{host}:{port}/docs")
    print(f"🔄 Auto-reload: {'Enabled' if reload else 'Disabled'}")
    print(f"📝 Log level: {log_level}")
    print("=" * 50)
    
    # Start uvicorn
    cmd = [
        sys.executable, "-m", "uvicorn", 
        "app.main:app",
        "--host", host,
        "--port", port,
        "--log-level", log_level
    ]
    
    if reload:
        cmd.append("--reload")
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def main():
    """Main function."""
    print("🔧 llm-core Local Development Server")
    print("=" * 50)
    
    # Check if we're in the correct directory
    if not Path("app/main.py").exists():
        print("❌ Error: Run this script from the llm-core project root")
        sys.exit(1)
    
    # Load environment variables
    load_env()
    
    # Install dependencies
    install_dependencies()
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()