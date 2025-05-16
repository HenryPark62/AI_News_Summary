import ollama
from .summarizer_strategy import SummarizerStrategy

class LocalSummarizer(SummarizerStrategy):
    def summarize(self, text, style):
        from .summarizer import create_prompt
        prompt = create_prompt(text, style)
        response = ollama.chat(
            model="gemma3:1b",  # 로컬에 설치한 모델명
            messages=[
                {"role": "system", "content": "당신은 뉴스 요약 전문가입니다."},
                {"role": "user", "content": prompt}
            ]
        )
        return response["message"]["content"].strip()
