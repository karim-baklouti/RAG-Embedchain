# Base Python image
FROM langchain/langchain

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt --timeout 1000

# Copy the application code
COPY . /app/

# Run the FastAPI application
CMD ["gunicorn", "-w", "3", "-k", "uvicorn.workers.UvicornWorker", "llm:app", "--bind", "0.0.0.0:8080", "--timeout", "10000"]