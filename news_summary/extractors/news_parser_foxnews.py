import requests
from bs4 import BeautifulSoup
from .base_extractor import BaseNewsExtractor

class FoxNewsExtractor(BaseNewsExtractor):
    def fetch(self, url: str) -> str:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        return res.text

    def parse(self, html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        # 모든 <p> 태그에서 텍스트 추출
        paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
        # 너무 짧은 <p>는 제외 (예: 광고, 공백 등)
        paragraphs = [p for p in paragraphs if len(p) > 20]
        if paragraphs:
            return "\n".join(paragraphs)
        return "본문 영역을 찾을 수 없습니다."
