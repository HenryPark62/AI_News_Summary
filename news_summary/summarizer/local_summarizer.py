import ollama
from .summarizer_strategy import SummarizerStrategy

class LocalSummarizer(SummarizerStrategy):
    def summarize(self, text, style):
        from .summarizer import create_prompt
        prompt = create_prompt(text, style)
        response = ollama.chat(
            model="llama3.1:8b",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"].strip()