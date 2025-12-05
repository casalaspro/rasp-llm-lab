# LLM Core Service

A well-structured FastAPI-based service for text generation using Language Models.

## 🏗️ Project Structure

```
llm-core/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration management
│   ├── models.py            # Pydantic models for API
│   └── routes.py            # API route handlers
├── .env                     # Environment variables (local)
├── requirements.txt         # Python dependencies
├── Dockerfile              # Container configuration
├── run_local.py            # Python startup script
└── start-local.ps1         # PowerShell startup script
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip package manager

### Local Development

#### Option 1: PowerShell Script (Recommended for Windows)
```powershell
.\start-local.ps1
```

#### Option 2: Python Script
```bash
python run_local.py
```

#### Option 3: Manual Commands
```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```

## 📡 API Endpoints

Once the server is running, you can access:

- **Server**: `http://127.0.0.1:8001`
- **Interactive API Docs**: `http://127.0.0.1:8001/docs`
- **Alternative API Docs**: `http://127.0.0.1:8001/redoc`

### Available Endpoints

#### Health Check
- **GET** `/` - Basic service information
- **GET** `/health` - Detailed health check

#### Text Generation
- **POST** `/generate` - Generate text from a prompt

#### Example Usage

```bash
# Health check
curl http://127.0.0.1:8001/

# Generate text
curl -X POST http://127.0.0.1:8001/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Hello, how are you?",
    "max_tokens": 100,
    "temperature": 0.7
  }'
```

## ⚙️ Configuration

The application uses environment variables for configuration. Copy and modify the `.env` file:

```bash
# Application settings
APP_NAME=llm-core
APP_VERSION=1.0.0
ENVIRONMENT=development

# Server settings
HOST=0.0.0.0
PORT=8001

# Debug settings
DEBUG=true
LOG_LEVEL=info

# Future LLM settings
# LLM_MODEL=your-model-name
# LLM_API_KEY=your-api-key
# LLM_MAX_TOKENS=1000
# LLM_TEMPERATURE=0.7
```

## 🐳 Docker

Build and run with Docker:

```bash
# Build the image
docker build -t llm-core .

# Run the container
docker run -p 8001:8001 llm-core
```

## 🧪 Testing

The service currently returns mock responses for testing pipeline integration between services. This will be replaced with actual LLM integration in the future.

## 🏗️ Architecture

- **config.py**: Centralized configuration using Pydantic Settings
- **models.py**: API request/response models with validation
- **routes.py**: Clean separation of route handlers
- **main.py**: FastAPI application setup and configuration

## 🔜 Future Enhancements

- Real LLM integration (OpenAI, Anthropic, local models)
- Authentication and rate limiting
- Request/response caching
- Metrics and monitoring
- Async request processing