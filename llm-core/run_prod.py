#!/usr/bin/env python3
"""
Run server in PRODUCTION mode.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import uvicorn

# 👇 Forziamo la modalità production
os.environ["APP_ENV"] = "prod"


def load_env():
    """Load environment variables from env.prod"""
    env_file = Path("env.prod")

    if env_file.exists():
        load_dotenv(env_file)
        print(f"📋 Loaded environment from {env_file}")
    else:
        print("❌ env.prod not found!")
        sys.exit(1)


def main():
    print("🏭 Starting llm-core (PRODUCTION)")
    print("=" * 50)

    if not Path("app/main.py").exists():
        print("❌ Run this script from the project root")
        sys.exit(1)

    load_env()

    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8001"))
    log_level = os.getenv("LOG_LEVEL", "info")
    reload = False  # in produzione non si usa reload

    print(f"🚀 Production server at http://{host}:{port}")
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
