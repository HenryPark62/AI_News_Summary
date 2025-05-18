# summarizer/summarizer_factory.py

# 추상 팩토리 패턴: 다양한 요약 전략 인스턴스를 선택적으로 생성

from abc import ABC, abstractmethod
from .summarizer_strategy import SummarizerStrategy
from .perplexity_proxy import PerplexityProxy
from .together_proxy import TogetherProxy
# 필요 시 다른 요약기 프록시도 import (e.g., OpenAIProxy)

# 추상 팩토리
class SummarizerFactory(ABC):
    @abstractmethod
    def create_summarizer(self) -> SummarizerStrategy:
        pass

# Perplexity용 팩토리
class PerplexityFactory(SummarizerFactory):
    def create_summarizer(self) -> SummarizerStrategy:
        return PerplexityProxy()

# Together용 팩토리    
class TogetherFactory(SummarizerFactory):
    def create_summarizer(self) -> SummarizerStrategy:
        return TogetherProxy()


# 팩토리 선택 함수

def get_summarizer_factory(model_name: str) -> SummarizerFactory:
    
    # Perplexity
    if model_name == "perplexity":
        return PerplexityFactory()
    
    # Together
    if model_name == "together":
        return TogetherFactory()

    else:
        return PerplexityFactory()  # 기본값
