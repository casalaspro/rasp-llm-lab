FROM python:3.11-slim

# 1) it sets the work directori inside the container
WORKDIR /app

# 2) it copies the requirements and installs them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3) it copies the app code
COPY app ./app

# 4) it starts uvicorn exposing the API on 0.0.0.0:8001
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]