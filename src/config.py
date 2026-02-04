import os
from dotenv import load_dotenv

load_dotenv()

# Ollama LLM Configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "mistral")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROMA_DB_URL = os.getenv("CHROMA_DB_URL", "http://chroma:8000")
DOCUMENTS_PATH = os.path.join(BASE_DIR, os.getenv("DOCUMENTS_PATH", "documents"))

# Chunking Configuration
CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# Create necessary directories
os.makedirs(DOCUMENTS_PATH, exist_ok=True)

# Validation
if not OLLAMA_BASE_URL:
    raise ValueError("❌ OLLAMA_BASE_URL is not set. Please add it to .env file")
