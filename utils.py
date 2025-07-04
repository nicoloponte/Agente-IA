import os
from dotenv import load_dotenv

def load_env():
    load_dotenv()
    ollama_base_url = os.getenv("OLLAMA_BASE_URL")
    if not ollama_base_url:
        raise ValueError("OLLAMA_BASE_URL no está definido en .env")
    return ollama_base_url

if __name__ == "__main__":
    url = load_env()
    print(f"OLLAMA_BASE_URL: {url}")