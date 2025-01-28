 # Kubernetes Deployment and Service Configuration 

This document explains the structure and purpose of the Kubernetes YAML configuration for deploying a RAG-LLM (Retrieval-Augmented Generation - Large Language Model) application. The configuration includes Deployments, Services, and Persistent Volumes for the frontend, backend, and Chroma database components.

---

## Overview

The application consists of three main components:
1. **Frontend**: A Streamlit-based user interface.
2. **Backend**: A large language model (LLM) serving as the backend.
3. **Chroma**: A vector database for storing and retrieving embeddings.

Each component is deployed as a Kubernetes `Deployment` and exposed via a `Service`. Additionally, Chroma uses a `PersistentVolume` and `PersistentVolumeClaim` for data storage.

---

## Namespace

All resources are deployed in the `rag-bot` namespace:
```yaml
namespace: rag-bot