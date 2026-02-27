
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the worker code
COPY . .

# Run the worker script (assumes it's executable standalone)
CMD ["python", "main.py"]