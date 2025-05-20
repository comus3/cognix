class BufferMemory:
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
        conversation = ""
        for msg in self.history:
            if msg["role"] == "system":
                continue  # Don't include the system message in the chat history here
            role = "Human" if msg["role"] == "user" else "AI"
            conversation += f"{role}: {msg['content']}\n"
        prompt = (
            f"{self.system_prompt.strip()}\n\n" if self.system_prompt else ""
        ) + (
            "The following is a friendly conversation between a human and an AI. "
            "The AI is talkative and provides lots of specific details from its context. "
            "If the AI does not know the answer to a question, it truthfully says it does not know.\n\n"
            f"Current conversation:\n{conversation}Human: "
        )
        print(f"DEBUG: \n ############### \n {prompt}  \n ############### \n")
        return prompt


    def reset(self):
        self.history = []
        if self.system_prompt:
            self.history.append({"role": "system", "content": self.system_prompt})

    def get_history(self):
        return self.history
