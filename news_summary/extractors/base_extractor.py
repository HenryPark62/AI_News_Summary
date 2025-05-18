# extractors/base_extractor.py

# 템플릿 메서드 패턴 기반 뉴스 본문 추출 상위 클래스

from abc import ABC, abstractmethod

class BaseNewsExtractor(ABC):
    def extract(self, url: str) -> str:
        """
        뉴스 기사 URL로부터 본문 텍스트를 추출하는 전체 흐름 정의
        """
        raw_html = self.fetch(url)
        clean_text = self.parse(raw_html)
        return self.postprocess(clean_text)

    @abstractmethod
    def fetch(self, url: str) -> str:
        """뉴스 원문 HTML을 가져옴"""
        pass

    @abstractmethod
    def parse(self, html: str) -> str:
        """HTML에서 기사 본문만 추출"""
        pass

    def postprocess(self, text: str) -> str:
        """공통 후처리 (공백 정리 등)"""
        return text.strip().replace("\xa0", " ")
