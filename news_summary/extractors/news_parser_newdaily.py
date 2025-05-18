# extractors/news_parser_newdaily.py

# NewDaily 뉴스 기사 전용 파서 (BaseNewsExtractor 상속)

import requests
from bs4 import BeautifulSoup
from .base_extractor import BaseNewsExtractor

class NewDailyNewsExtractor(BaseNewsExtractor):
    def fetch(self, url: str) -> str:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        return res.text

    def parse(self, html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")

        # 뉴데일리 본문은 class="article_content" div 내부에 있음
        body = soup.find("div", class_="article_content")
        if body:
            return body.get_text()
        return "❌ 본문 영역을 찾을 수 없습니다."