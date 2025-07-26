import os
import requests
from dotenv import load_dotenv

# Load API key
load_dotenv("Assets/.env")
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL_NAME = os.getenv("OPENROUTER_MODEL")

# OpenRouter endpoint (OpenAI-compatible)
API_URL = "https://openrouter.ai/api/v1/chat/completions"

def ask_llm(prompt: str, max_tokens: int = 500) -> str:
    """
    Sends the prompt to the LLM and returns the response.
    """
    if not API_KEY:
        raise EnvironmentError("Missing OPENROUTER_API_KEY in .env file.")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://chat.openai.com",  # Optional, for OpenRouter
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that only answers based on the given document."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": max_tokens,
        "temperature": 0.2  # Lower = more focused and factual
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except requests.exceptions.RequestException as e:
        return f"❌ API Error: {str(e)}"
    except KeyError:
        return "❌ Unexpected API response format."

