FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the port for the API
EXPOSE 5000

# Default command starts the API
CMD ["python", "api.py"]

# Use this command to start the CLI instead:
# CMD ["python", "main.py"]