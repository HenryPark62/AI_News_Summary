# summarizer/summarizer_strategy.py

# 전략 패턴의 핵심 인터페이스
from abc import ABC, abstractmethod

class SummarizerStrategy(ABC):
    @abstractmethod
    def summarize(self, text: str, style: str) -> str:
        """
        주어진 텍스트를 특정 스타일에 따라 요약하는 전략 메서드
        :param text: 원문 텍스트
        :param style: 'brief', 'detailed' 등 요약 스타일
        :return: 요약된 문자열 결과
        """
        pass
