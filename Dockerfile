# Use Python 3.9 as base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files into the container (all files from your project, including the 'app' folder)
COPY . /app/

# Create cache directory and set permissions
RUN mkdir -p /tmp/.cache/huggingface && \
    chmod -R 777 /tmp/.cache

# Set environment variable
ENV TRANSFORMERS_CACHE=/tmp/.cache/huggingface

# Expose ports for REST (5000) and gRPC (50051)
EXPOSE 5000 50051

# Set the command to run the app
CMD ["python", "app/app.py"]
