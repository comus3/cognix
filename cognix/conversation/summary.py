class SummaryMemory:
    def __init__(self, summarizer, system_prompt=None, max_recent=4):
        self.summarizer = summarizer
        self.system_prompt = system_prompt
        self.summary = ""  # Keep summary separate from system_prompt
        self.recent_history = []
        self.max_recent = max_recent

    def add_user_message(self, content: str):
        self.recent_history.append({"role": "user", "content": content})
        self._prune_recent_entries()

    def add_assistant_message(self, content: str):
        self.recent_history.append({"role": "assistant", "content": content})
        self._prune_recent_entries()

    def _prune_recent_entries(self):
        if len(self.recent_history) > self.max_recent:
            self._update_summary()
            self.recent_history = self.recent_history[-self.max_recent:]


            
    def _format_new_lines(self) -> str:
        lines = []
        for msg in self.recent_history:
            if msg["role"] == "user":
                lines.append(f"User:\n{msg['content']}")
            else:
                lines.append(f"{msg['content']}") 
        return "\n\n".join(lines)
    
    def _last_user_message(self) -> str:
        for msg in reversed(self.recent_history):
            if msg["role"] == "user":
                return msg["content"]
        return ""
    def _last_assistant_message(self) -> str:
        for msg in reversed(self.recent_history):
            if msg["role"] == "assistant":
                return msg["content"]
        return ""

    def _update_summary(self):
        new_lines = self._format_new_lines()
        prompt = f"""You are an AI assistant tasked with summarizing a conversation between a User and an Assistant. Only summarize the Assistant's responses.

        Your goal is to produce a concise, comprehensive summary that captures all important details without losing any information.  
        The summary must be a single continuous block of text with no lists, comments, or formatting.  
        Do not include any explanations, quotes, or extra commentary.

        Current summary:
        {self.summary.strip()}

        New dialogue:
        {new_lines}"""

        self.summary = self.summarizer(prompt).strip()



    def get_prompt(self) -> str:
        prompt_parts = []
        if self.system_prompt:
            prompt_parts.append(f"[SYSTEM] {self.system_prompt.strip()}")
        if self.summary:
            prompt_parts.append(f"[ASSISTANT] {self.summary.strip()}")
        if self.recent_history:
            prompt_parts.append(f"[USER] {self._last_user_message()}")
        prompt = "\n\n".join(prompt_parts)

        print(f"DEBUG:\n###############\n{prompt}\n###############\n")
        return prompt
    


    def reset(self):
        self.summary = ""
        self.recent_history = []

    def get_history(self):
        return {"summary": self.summary}
