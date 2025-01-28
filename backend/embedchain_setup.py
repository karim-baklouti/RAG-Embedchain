import os
import logging
from embedchain import App
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
huggingface_token = os.getenv("HUGGINGFACE_ACCESS_TOKEN")
if not huggingface_token:
    raise ValueError("HUGGINGFACE_ACCESS_TOKEN not found in .env file")
os.environ["HUGGINGFACE_ACCESS_TOKEN"] = huggingface_token

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
    'vectordb': {
        'provider': 'chroma',
        'config': {
            'collection_name': 'llm-store',
            'host': 'chroma-service',  # you can use localhost or you can comment this when working with local chroma db
            'port': 8000,        
            'allow_reset': True
        }
    }
}

def initialize_app():
    """Initialize the Embedchain app and add documents."""
    try:
        app_embedchain = App.from_config(config=config)
        logger.info("Embedchain app initialized successfully.")

        # Add local PDF files
        pdf_files = ["./data/09_mlops.pdf", "./data/TheBigBook.pdf"]
        for pdf_file in pdf_files:
            if not os.path.exists(pdf_file):
                logger.warning(f"File not found: {pdf_file}")
                continue
            app_embedchain.add(pdf_file, data_type="pdf_file")
            logger.info(f"Added PDF file: {pdf_file}")

        # Add web pages
        urls = [
            "https://ml-ops.org/content/mlops-principles",
            "https://ml-ops.org/content/three-levels-of-ml-software",
            "https://ml-ops.org/content/mlops-stack-canvas",
            "https://ml-ops.org/content/model-governance",
            "https://ml-ops.org/content/end-to-end-ml-workflow"
        ]
        for url in urls:
            app_embedchain.add(url, data_type="docs_site")
            logger.info(f"Added web page: {url}")

        logger.info("All documents added successfully.")
        return app_embedchain

    except Exception as e:
        logger.error(f"Error initializing Embedchain app: {e}")
        raise

