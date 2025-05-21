from cognix.backend.ollama_backend import OllamaBackend

from cognix.conversation.manager import ConversationManager

from cognix.utils.const.PROMPTS.conversation import BASE_CONVERSATION_PROMPT
from cognix.utils.const.registry import MemoryRegistry

class COGNIXSession:
    def __init__(self, model="llama2", system_prompt=BASE_CONVERSATION_PROMPT, memory_type="summary",memory_config=None):
        self.backend = OllamaBackend(model=model)

        # Use the registry to get the memory instance dynamically
        memory = MemoryRegistry.get(memory_type, memory_config)

        self.conv_manager = ConversationManager(memory=memory, system_prompt=system_prompt)


    def chat(self, user_input: str, **kwargs) -> str:
        self.conv_manager.add_user_message(user_input)
        prompt = self.conv_manager.get_prompt()
        response = self.backend.generate(prompt=prompt, **kwargs)
        self.conv_manager.add_assistant_message(response)
        return response
    
    def chat_stream(self, user_input: str, **kwargs):
        self.conv_manager.add_user_message(user_input)
        prompt = self.conv_manager.get_prompt()
        stream = self.backend.generate_stream(prompt=prompt, **kwargs)
        full_response = ""
        for chunk in stream:
            full_response += chunk
            yield chunk
        self.conv_manager.add_assistant_message(full_response)

    def reset(self):
        self.conv_manager.reset()

    def set_system_prompt(self, prompt: str):
        self.conv_manager.system_prompt = prompt
        self.reset()

    def get_history(self):
        return self.conv_manager.get_history()
