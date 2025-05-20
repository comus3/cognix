from abc import ABC, abstractmethod

class MemoryStrategy(ABC):
    @abstractmethod
    def add_message(self, role: str, content: str):
        pass

    @abstractmethod
    def get_prompt(self) -> str:
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def get_state(self) -> dict:
        pass
