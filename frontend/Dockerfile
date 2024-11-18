# Use the official Python base image with a specific version
FROM python:3.12-slim

# Set working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files to the container
COPY . .

# cmd to run streamlit
CMD streamlit run --server.port $PORT app.py 