class ConversationManager:
    def __init__(self, system_prompt=None, max_history=20):
        self.system_prompt = system_prompt
        self.max_history = max_history
        self.history = []
        if system_prompt:
            self.history.append({"role": "system", "content": system_prompt})

    def add_user_message(self, content: str):
        self.history.append({"role": "user", "content": content})
        self._trim_history()

    def add_assistant_message(self, content: str):
        self.history.append({"role": "assistant", "content": content})
        self._trim_history()

    def _trim_history(self):
        if len(self.history) > self.max_history + 1:
            self.history = [self.history[0]] + self.history[-self.max_history:]

    def get_prompt(self) -> str:
        prompt = ""
        for msg in self.history:
            prompt += f"{msg['role'].capitalize()}: {msg['content']}\n"
        prompt += "Assistant: "
        return prompt

    def reset(self):
        self.history = []
        if self.system_prompt:
            self.history.append({"role": "system", "content": self.system_prompt})

    def get_history(self):
        return self.history
