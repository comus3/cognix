from cognix.backend.ollama_backend import OllamaBackend
from cognix.conversation.manager import ConversationManager

class COGNIXSession:
    def __init__(self, model="llama2", system_prompt=None):
        self.backend = OllamaBackend(model=model)
        self.conv_manager = ConversationManager(system_prompt=system_prompt)

    def chat(self, user_input: str) -> str:
        self.conv_manager.add_user_message(user_input)
        prompt = self.conv_manager.get_prompt()
        response = self.backend.generate(prompt)
        self.conv_manager.add_assistant_message(response)
        return response

    def reset(self):
        self.conv_manager.reset()

    def set_system_prompt(self, prompt: str):
        self.conv_manager.system_prompt = prompt
        self.reset()

    def get_history(self):
        return self.conv_manager.get_history()
