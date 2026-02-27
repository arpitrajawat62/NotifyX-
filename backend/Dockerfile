
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code
COPY app/ app/

# Expose FastAPI port (default 8000)
EXPOSE 8000

# Run with Uvicorn (adjust if your entry point is different, e.g., app.main:app)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]