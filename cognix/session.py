from cognix.backend.ollama_backend import OllamaBackend
from cognix.conversation.buffer import BufferMemory
from cognix.conversation.summary import SummaryMemory

from cognix.utils.const.PROMPTS.conversation import BASE_CONVESATION_PROMPT

class COGNIXSession:
    def __init__(self, model="llama2", system_prompt=BASE_CONVESATION_PROMPT, memory_type="summary"):
        self.backend = OllamaBackend(model=model)

        if memory_type == "summary":
            self.conv_manager = SummaryMemory(
                summarizer=self._summarizer,
                system_prompt=system_prompt
            )
        else:
            self.conv_manager = BufferMemory(system_prompt=system_prompt)

    def _summarizer(self, prompt: str) -> str:
        return self.backend.generate(prompt = prompt)

    def chat(self, user_input: str, **kwargs) -> str:
        self.conv_manager.add_user_message(user_input)
        prompt = self.conv_manager.get_prompt()
        response = self.backend.generate(prompt=prompt, **kwargs)
        self.conv_manager.add_assistant_message(response)
        return response

    def reset(self):
        self.conv_manager.reset()

    def set_system_prompt(self, prompt: str):
        self.conv_manager.system_prompt = prompt
        self.reset()

    def get_history(self):
        return self.conv_manager.get_history()

    def chat_stream(self, user_input: str, **kwargs):
        self.conv_manager.add_user_message(user_input)
        prompt = self.conv_manager.get_prompt()
        stream = self.backend.generate_stream(prompt=prompt, **kwargs)
        full_response = ""
        for chunk in stream:
            full_response += chunk
            yield chunk
        self.conv_manager.add_assistant_message(full_response)
