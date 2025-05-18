# summarizer/together_summarizer.py
# ✅ RealSubject: Together API 요청 처리 전략 

import requests
from .summarizer_strategy import SummarizerStrategy
from .prompt_utils import create_prompt

class TogetherSummarizer(SummarizerStrategy):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.url = "https://api.together.xyz/v1/chat/completions"

    def summarize(self, text, style):
        if style not in ("brief", "detailed"):
            return f"[Together 오류] 지원하지 않는 스타일: {style}"

        prompt = create_prompt(text, style)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "messages": [
                {"role": "system", "content": "당신은 뉴스 요약 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 800 if style == "detailed" else 500,
            "temperature": 0.3,
            "top_p": 0.95
        }

        try:
            response = requests.post(self.url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"[Together API 오류] {str(e)}"