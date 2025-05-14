# summarizer.py

import openai
import ollama

# OpenAI API 키 설정
openai.api_key = "너의 OpenAI API 키 입력"

# ==========================
# 전략 패턴 기반 요약기 클래스들
# ==========================

class SummarizerStrategy:
    def summarize(self, text, style):
        raise NotImplementedError

# 1. OpenAI GPT 기반 요약기
class OpenAISummarizer(SummarizerStrategy):
    def summarize(self, text, style):
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

# 2. Together.ai 무료 모델 기반 요약기 (예시)
class TogetherSummarizer(SummarizerStrategy):
    def summarize(self, text, style):
        prompt = create_prompt(text, style)
        # 여기에 실제 Together API 호출 가능
        return f"🔧 (예시) Together.ai 모델로 {style} 스타일 요약 완료"

# 3. 로컬 LLM (Ollama 등) 기반 요약기
class LocalSummarizer(SummarizerStrategy):
    def summarize(self, text, style):
        prompt = create_prompt(text, style)
        response = ollama.chat(
            model="llama3.1:8b",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["message"]["content"].strip()

# ==========================
# Summarizer 선택 함수
# ==========================

def get_summarizer(model_name):
    if model_name == "openai":
        return OpenAISummarizer()
    elif model_name == "together":
        return TogetherSummarizer()
    elif model_name == "local":
        return LocalSummarizer()
    else:
        return OpenAISummarizer()  # 기본값

# ==========================
# 프롬프트 생성 함수 (스타일별)
# ==========================

def create_prompt(text, style):
    if style == "brief":
        return (
            "다음은 뉴스 기사 전문입니다.\n\n"
            f"{text}\n\n"
            "이 뉴스를 한국어로 간결하고 핵심만 요약해 주세요. (2~3줄 이내)"
        )
    elif style == "detailed":
        return (
            "다음은 뉴스 기사 전문입니다.\n\n"
            f"{text}\n\n"
            "이 뉴스를 한국어로 상세하고 풍부하게 요약해 주세요. (5~7줄 정도)"
        )
    else:
        # 기본은 간결 요약
        return (
            "다음은 뉴스 기사 전문입니다.\n\n"
            f"{text}\n\n"
            "이 뉴스를 한국어로 간결하고 명확하게 3~5줄 이내로 요약해 주세요."
        )

# ==========================
# 메인 요약 함수
# ==========================

def summarize_news(text, model_name="openai", style="brief"):
    summarizer = get_summarizer(model_name)
    return summarizer.summarize(text, style)