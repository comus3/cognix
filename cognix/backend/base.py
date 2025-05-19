from abc import ABC, abstractmethod

class BaseBackend(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass

class OllamaBackend(BaseBackend):
    def __init__(self, model):
        self.model = model
        # init connection stuff

    def generate(self, prompt: str) -> str:
        # call ollama CLI or python lib here
        return "ollama response"
