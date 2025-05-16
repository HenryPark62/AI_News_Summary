import os
import requests
from .summarizer_strategy import SummarizerStrategy

api_key = "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"

class PerplexitySummarizer(SummarizerStrategy):
    def summarize(self, text, style):
        from .summarizer import create_prompt
        prompt = create_prompt(text, style)

        url = "https://api.perplexity.ai/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "sonar-pro",  # 또는 pplx-7b-online 등 지원 모델명
            "messages": [
                {"role": "system", "content": "당신은 뉴스 요약 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 800 if style == "detailed" else 500
        }
        response = requests.post(url, headers=headers, json=data, timeout=30)
        if response.status_code != 200:
            return f"[Perplexity API 오류] status {response.status_code}: {response.text}"
        result = response.json()
        if 'choices' in result and result['choices']:
            return result['choices'][0]['message']['content'].strip()
        elif 'error' in result:
            return f"[Perplexity API 오류] {result['error']}"
        else:
            return f"[Perplexity API 알 수 없는 오류] 응답: {result}"
