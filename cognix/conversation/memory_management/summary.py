from cognix.conversation.memory_management.memory_strategy import MemoryStrategy
import threading

class SummaryMemory(MemoryStrategy):
    def __init__(self, summarizer, max_recent=4):
        self.summarizer = summarizer
        self.summary = ""
        self.recent_history = []
        self.max_recent = max_recent

    def add_message(self, role: str, content: str):
        self.recent_history.append({"role": role, "content": content})
        self._prune_recent_entries()

    def _prune_recent_entries(self):
        if len(self.recent_history) > self.max_recent:
            self._update_summary_async()
            self.recent_history = [self._last_user_message()]

    def _last_user_message(self):
        return next((msg for msg in reversed(self.recent_history) if msg["role"] == "user"), "")

    def _format_new_lines(self) -> str:
        return "\n\n".join(
            f"[USER] {m['content']}" if m["role"] == "user" else f"[CHATBOT] {m['content']}"
            for m in self.recent_history
        )

    def _update_summary(self):
        new_lines = self._format_new_lines()
        prompt = f"""
        Can you please summarize the following conversation and provide a brief overview of the main points discussed?
        I want only the summary of the conversation, not the conversation itself.
        {self.summary.strip()}
        {new_lines}"""
        self.summary = self.summarizer(prompt).strip()
        
    def _update_summary_async(self):
        def summarization_task():
            new_lines = self._format_new_lines()
            prompt = f"""
            Can you please summarize the following conversation and provide a brief overview of the main points discussed?
            I want only the summary of the conversation, not the conversation itself.
            {self.summary.strip()}
            {new_lines}"""
            new_summary = self.summarizer(prompt).strip()
            self.summary = new_summary  # safely update shared state

        thread = threading.Thread(target=summarization_task, daemon=True)
        thread.start()

    def get_prompt(self) -> str:
        parts = []
        if self.summary:
            parts.append(f"[SUMMARY] {self.summary.strip()}")
        if self.recent_history:
            parts.append(self._format_new_lines().strip())
        parts.append("\n[CHATBOT] ")
        return "\n\n".join(parts)

    def reset(self):
        self.summary = ""
        self.recent_history = []

    def get_state(self):
        return {"summary": self.summary}

    
def summary_memory_factory(config):
    return SummaryMemory(**config)