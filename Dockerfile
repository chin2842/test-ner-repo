# Use Python 3.9 as base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Install PyTorch (or TensorFlow) for model inference
RUN pip install torch

# Copy the application files into the container (all files from your project, including the 'app' folder)
COPY . /app/

# Create cache directory and set permissions for Hugging Face model cache
RUN mkdir -p /tmp/.cache/huggingface && \
    chmod -R 777 /tmp/.cache

# Set environment variable for Hugging Face cache
ENV TRANSFORMERS_CACHE=/tmp/.cache/huggingface

# Expose ports for REST (5000) and gRPC (50051)
EXPOSE 5000 50051

# Set the command to run the app
CMD ["python", "app/app.py"]
