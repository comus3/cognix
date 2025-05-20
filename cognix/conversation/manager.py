from cognix.conversation.memory_management.memory_strategy import MemoryStrategy

class ConversationManager:
    def __init__(self, memory: MemoryStrategy, system_prompt=None):
        self.memory = memory
        self.system_prompt = system_prompt

    def add_user_message(self, content: str):
        self.memory.add_message("user", content)

    def add_assistant_message(self, content: str):
        self.memory.add_message("assistant", content)

    def get_prompt(self) -> str:
        return self.memory.get_prompt()

    def reset_conversation(self):
        self.memory.reset()

    def export_state(self):
        return self.memory.get_state()
