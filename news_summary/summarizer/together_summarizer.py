import requests
from .summarizer_strategy import SummarizerStrategy

TOGETHER_API_KEY = "b108677089b439b4be4e5813d688b34108923858b98dd2c6cb6b54ce8f009c5a"

class TogetherSummarizer(SummarizerStrategy):
    def summarize(self, text, style):
        from .summarizer import create_prompt
        prompt = create_prompt(text, style)

        url = "https://api.together.xyz/v1/chat/completions"  # Url
        headers = {
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",  # Together 무료 제공 모델 사용 예시
            "messages": [
                {"role": "system", "content": "당신은 뉴스 요약 전문가입니다."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 800 if style == "detailed" else 500
        }

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        result = response.json()
        return result['choices'][0]['message']['content'].strip()
    




    