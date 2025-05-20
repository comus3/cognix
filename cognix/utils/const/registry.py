# constants/registry.py

from cognix.conversation.memory_management.summary import summary_memory_factory
from cognix.conversation.memory_management.buffer import buffer_memory_factory



class MemoryRegistry:
    _registry = {}

    @classmethod
    def register(cls, name):
        def wrapper(factory_fn):
            cls._registry[name] = factory_fn
            return factory_fn
        return wrapper

    @classmethod
    def get(cls, name, config):
        if name not in cls._registry:
            raise ValueError(f"Memory type '{name}' not found.")
        return cls._registry[name](config)

    @classmethod
    def list(cls):
        return list(cls._registry.keys())



MEMORY_REGISTRY = {
    "summary": lambda config: SummaryMemory(
        summarizer=config["summarizer"],
        config=config
    ),
    "buffer": lambda config: BufferMemory(config=config),
}
MemoryRegistry.register("summary")(summary_memory_factory)
MemoryRegistry.register("buffer")(buffer_memory_factory)
