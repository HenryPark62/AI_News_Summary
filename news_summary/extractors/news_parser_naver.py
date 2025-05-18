# extractors/news_parser_naver.py

# Naver 뉴스 기사 전용 파서 (BaseNewsExtractor 상속)
# 네이버 제휴 언론사 (구독 가능한)는 html이 모두 공통된 구조라 하나의 extractors로 추출 가능합니다.

import requests
from bs4 import BeautifulSoup
from .base_extractor import BaseNewsExtractor

class NaverNewsExtractor(BaseNewsExtractor):
    def fetch(self, url: str) -> str:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        return res.text

    def parse(self, html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")

        # 네이버 뉴스 본문 div id는 'dic_area' 또는 'newsct_article'
        body = soup.find("div", id="dic_area")
        if body is None:
            body = soup.find("div", id="newsct_article")
        if body:
            return body.get_text()
        return "본문 영역을 찾을 수 없습니다."
