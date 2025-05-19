import subprocess
import json
from cognix.backend.base import BaseBackend

class OllamaBackend(BaseBackend):
    def __init__(self, model: str):
        self.model = model

    def generate(self, prompt: str) -> str:
        # Call ollama CLI to get response from the model
        # Example: ollama generate <model> --prompt "<prompt>"

        try:
            result = subprocess.run(
                ["ollama", "run", self.model, prompt],
                capture_output=True,
                text=True,
                check=True
            )
            # Ollama CLI prints the response directly
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            # Handle errors cleanly
            raise RuntimeError(f"Ollama generate failed: {e.stderr.strip()}") from e
