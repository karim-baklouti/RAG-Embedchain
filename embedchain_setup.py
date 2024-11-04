import os
from embedchain import App
from dotenv import load_dotenv


# Set your Hugging Face token
load_dotenv()
os.environ["HUGGINGFACE_ACCESS_TOKEN"] = os.getenv("HUGGINGFACE_ACCESS_TOKEN")

# Embedchain configuration
config = {
    'llm': {
        'provider': 'huggingface',
        'config': {
            'model': 'mistralai/Mistral-7B-Instruct-v0.2',
            'top_p': 0.1
        }
    },
    'embedder': {
        'provider': 'huggingface',
        'config': {
            'model': 'sentence-transformers/all-MiniLM-L6-v2'
        }
    },
    'chunker': {
        'chunk_size': 2000,
        'chunk_overlap': 50,
        'length_function': 'len',
        'min_chunk_size': 51
    },
}

def initialize_app():
    """Initialize the Embedchain app and add documents."""
    app_embedchain = App.from_config(config=config)

    # Add documents (PDF and CSV files)
    app_embedchain.add("./data/09_mlops.pdf", data_type="pdf_file")
    app_embedchain.add("./data/TheBigBook.pdf",data_type="pdf_file")

    app_embedchain.add("https://ml-ops.org/content/mlops-principles", data_type="docs_site")
    app_embedchain.add("https://ml-ops.org/content/three-levels-of-ml-software", data_type="docs_site")
    app_embedchain.add("https://ml-ops.org/content/mlops-stack-canvas", data_type="docs_site")
    app_embedchain.add("https://ml-ops.org/content/model-governance", data_type="docs_site")
    app_embedchain.add("https://ml-ops.org/content/end-to-end-ml-workflow", data_type="docs_site")

    return app_embedchain
