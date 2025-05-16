import openai
from .summarizer_strategy import SummarizerStrategy

openai.api_key = "너의 OpenAI API 키 입력"

class OpenAISummarizer(SummarizerStrategy):
    def summarize(self, text, style):
        from .summarizer import create_prompt  # 순환 import 주의
        prompt = create_prompt(text, style)
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "당신은 뉴스 요약 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=800 if style == "detailed" else 500
        )
        return response['choices'][0]['message']['content'].strip()