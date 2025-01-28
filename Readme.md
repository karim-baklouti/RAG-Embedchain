# chatbot for MLOps with Embedchain

## Installation
### install Poetry
[Poetry installation](https://python-poetry.org/docs/)

### Go to root project
```bash
poetry install --no-root
```
## Configuration Details (backend/embedchain_setup.py)    
 Hugging Face Token: Replace "your_huggingface_token_here" with your actual Hugging Face access token.

   Model Configuration:
        Language Model (llm):
            Provider: huggingface
            Model: mistralai/Mistral-7B-Instruct-v0.2
            Top P: Controls the diversity of the generated outputs (higher values lead to more diverse results).
        Embedder:
            Provider: huggingface
            Model: sentence-transformers/all-MiniLM-L6-v2 for generating embeddings.
        Chunker:
            Chunk Size: The size of text chunks to be created from larger documents (set to 2000).
            Chunk Overlap: The number of overlapping tokens between chunks (set to 50).
            Length Function: The method used to determine the length of each chunk (set to len).
            Min Chunk Size: The minimum allowed size for a chunk to ensure meaningful data is maintained (set to 51).

   Document Types: The application supports adding documents in PDF ,Json, URL and  CSV formats. You can uncomment the CSV line to add a CSV file as well.


## FastApi(backend/llm.py)
This FastAPI application provides an interface for interacting with an Embedchain instance, which is used to process natural language queries. It also includes functionality for uploading files (PDF , JSON and CSV) to Embedchain's ChromaDB.

## Streamlit (frontend/app.py)
 chatbot interface in Streamlit that automatically handles multiple sessions, allowing users to chat with an assistant. The application interacts with a FastAPI endpoint to retrieve responses for user queries and automatically persists the chat history.

 ## Run The LLM
 ```bash
poetry run python llm.py
```

## Run the user Interface
```bash 
poetry run streamlit run app.py
```
## Screenshot about RestApi
![alt text](/screenshots/backend.png)
## Screenshots about user Interface
![alt text](/screenshots/image.png)

## Note:
We use requirements.txt instead of poetry in the dockerization because the image size is lighter !

# MLOPS(Docker and Kubernetes Workflow Documentation)

This documentation describes the workflow for defining, building, and deploying Docker images for projects using Kubernetes.

## Workflow Overview

1. **Define a Dockerfile for each project**:
   - Create a `Dockerfile` in the root directory of the project to specify the container image configuration.
   - The `Dockerfile` should include all dependencies and application runtime configurations.

2. **Push the Docker image to Docker Hub**:
   - Build the Docker image locally or in a CI/CD pipeline.
   - Tag the image with the appropriate repository and version.
   - Push the image to the designated Docker Hub registry.

3. **Organize Kubernetes deployment**:
   - Store Kubernetes manifests (e.g., deployment, service, config maps) under the [`k8s/`](k8s/) folder folder within the project directory.
