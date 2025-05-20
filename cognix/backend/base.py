from abc import ABC, abstractmethod

class BaseBackend(ABC):
    @abstractmethod
    def generate(self, **kwargs) -> str:
        """
        Generate a full response based on parameters.
        Parameters depend on the specific backend implementation.
        """
        pass

    @abstractmethod
    def generate_stream(self, **kwargs):
        """
        Generate a streamed response based on parameters.
        Yields chunks of the response.
        """
        pass
