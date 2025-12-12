#!/usr/bin/env python3
"""
Run server in LOCAL mode.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import uvicorn

# 👇 Forziamo l'ambiente PRIMA di caricare config.py
os.environ["APP_ENV"] = "local"


def load_env():
    """Load environment variables from env.local"""
    env_file = Path(".env.local")

    if env_file.exists():
        load_dotenv(env_file)
        print(f"📋 Loaded environment from {env_file}")
    else:
        print("❌ env.local not found!")
        sys.exit(1)


def main():
    print("🔧 Starting llm-core (LOCAL)")
    print("=" * 50)

    # Check directory
    if not Path("app/main.py").exists():
        print("❌ Run this script from the project root")
        sys.exit(1)

    # Load env
    load_env()

    # Read server config
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "8001"))
    log_level = os.getenv("LOG_LEVEL", "debug")
    reload = os.getenv("DEBUG", "true").lower() == "true"

    print(f"🚀 Local server at http://{host}:{port}")
    print("=" * 50)

    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        log_level=log_level,
        reload=reload,
    )


if __name__ == "__main__":
    main()
