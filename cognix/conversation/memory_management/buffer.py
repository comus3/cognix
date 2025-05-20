from cognix.conversation.memory_management.memory_strategy import MemoryStrategy

from cognix.utils.const.config import BUFFER_CONFIG

class BufferMemory(MemoryStrategy):
    def __init__(self, system_prompt: str = None, max_history: int = 20):
        self.system_prompt = system_prompt
        self.max_history = max_history
        self.history = []
        if system_prompt:
            self.history.append({"role": "system", "content": system_prompt})

    def add_message(self, role: str, content: str):
        if role not in {"user", "assistant"}:
            raise ValueError("Role must be 'user' or 'assistant'")
        self.history.append({"role": role, "content": content})
        self._trim_history()

    def add_user_message(self, content: str):
        self.add_message("user", content)

    def add_assistant_message(self, content: str):
        self.add_message("assistant", content)

    def get_prompt(self) -> str:
        conversation = ""
        for msg in self.history:
            if msg["role"] == "system":
                continue
            role = "[USER] " if msg["role"] == "user" else "[CHATBOT] "
            conversation += f"{role}{msg['content']}\n"
        prompt = conversation.strip() + "\n[CHATBOT] "
        return prompt

    def reset(self):
        self.history = []
        if self.system_prompt:
            self.history.append({"role": "system", "content": self.system_prompt})

    def get_state(self) -> dict:
        return {"history": self.history}

    def get_history(self):
        return self.history

    def _trim_history(self):
        system_msg = self.history[0] if self.history and self.history[0]["role"] == "system" else None
        messages = self.history[1:] if system_msg else self.history
        trimmed = messages[-self.max_history:]
        self.history = [system_msg] + trimmed if system_msg else trimmed


def buffer_memory_factory(config=BUFFER_CONFIG) -> BufferMemory:
    """
    Factory function to create a BufferMemory instance.
    :param config: Configuration dictionary for BufferMemory.
    :return: An instance of BufferMemory.
    """
    if config is None:
        config = BUFFER_CONFIG
    return BufferMemory(**config)
