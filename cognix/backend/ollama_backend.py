import requests
from cognix.backend.base import BaseBackend
import json

from cognix.utils.const.ENDPOINTS.llm import OLLAMA_API_URL_BASE, OLLAMA_API_URL_ENDPOINT

class OllamaBackend(BaseBackend):
    def __init__(self, model: str = None, api_url: str = OLLAMA_API_URL_BASE):
        self.model = model
        self.api_url = api_url

    def generate(self, **kwargs) -> str:
        url = self.api_url + OLLAMA_API_URL_ENDPOINT

        # Use model from kwargs or fallback to self.model
        model = kwargs.pop("model", self.model)
        if not model:
            raise ValueError("Model name must be specified either at init or as a parameter.")

        # Compose payload with mandatory model and prompt + rest of kwargs
        payload = {
            "model": model,
            **kwargs
        }

        # Force stream=True to handle streaming internally but return concatenated string
        payload["stream"] = True
        try:
            with requests.post(url, json=payload, stream=True) as response:
                response.raise_for_status()
                full_output = ""
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line.decode("utf-8"))
                        full_output += chunk.get("response", "")
                        if chunk.get("done"):
                            break
                return full_output.strip()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Ollama API request failed: {e}")

    def generate_stream(self, **kwargs):
        url = f"{self.api_url}/api/generate"

        model = kwargs.pop("model", self.model)
        if not model:
            raise ValueError("Model name must be specified either at init or as a parameter.")

        payload = {
            "model": model,
            **kwargs
        }

        # Default to stream True if not specified
        payload.setdefault("stream", True)
        try:
            with requests.post(url, json=payload, stream=payload["stream"]) as response:
                response.raise_for_status()
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line.decode("utf-8"))
                        if "response" in chunk:
                            yield chunk["response"]
                        if chunk.get("done"):
                            break
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Ollama streaming API request failed: {e}")
