# extractors/naver_parser_chosun.py
import requests
from bs4 import BeautifulSoup
import re

def extract_clean_news_body(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
    except requests.RequestException as e:
        return f"❌ 요청 실패: {e}"

    soup = BeautifulSoup(res.text, "html.parser")
    article = soup.find("article", id="dic_area")
    if not article:
        return "❌ 본문 태그가 없습니다."

# HTML 소스코드에서 불필요한 태그 제거
    for tag in article.find_all(["b", "em", "span", "figure", "div", "img"]): 
        tag.decompose()

    raw_text = article.get_text(separator="\n", strip=True)
    clean_text = re.sub(r'\s*/[^\n]+', '', raw_text)
    lines = clean_text.strip().split("\n")
    if len(lines) > 3:
        lines = lines[3:]
    return "\n".join(lines).strip()