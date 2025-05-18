# summarizer/summarizer.py

# 전략 실행 컨텍스트 + 프롬프트 생성 + 외부 진입점 함수

"""

사용자 요청
   ↓
summarize_news() → 팩토리에서 전략 프록시 생성
   ↓
create_prompt()로 프롬프트 생성
   ↓
strategy.summarize(prompt, style)
   ↓
프록시 → 실제 API 호출

"""

# 전략 실행 컨텍스트 + 외부 진입점 함수

from .summarizer_factory import get_summarizer_factory
from .prompt_utils import create_prompt  # 🔁 순환 참조 방지를 위해 별도 모듈로 분리

# =====================
# 전략 실행 컨텍스트
# =====================
class Summarizer:
    def __init__(self, strategy):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def summarize(self, text):
        return self.strategy.summarize(text)

# =====================
# 외부 진입점 함수
# =====================
def summarize_news(text, model_name="perplexity", style="brief"):
    factory = get_summarizer_factory(model_name)
    strategy = factory.create_summarizer()
    prompt = create_prompt(text, style)
    return strategy.summarize(prompt, style)

