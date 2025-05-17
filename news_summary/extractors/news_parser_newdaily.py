# extractors/naver_parser_newdaily.py
import requests
from bs4 import BeautifulSoup

def extract_clean_news_body(url: str) -> str:
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
    except requests.RequestException as e:
        return f"❌ 요청 실패: {e}"

    soup = BeautifulSoup(res.text, "html.parser")
    # 기사 본문은 <li class="par"> 내부의 여러 <div>에 나눠져 있음
    li_par = soup.find("li", class_="par")
    if not li_par:
        return "❌ 본문 태그(li.par)가 없습니다."

    # 본문 내용만 추출 (이미지/광고/스크립트 등 제외)
    paragraphs = []
    for div in li_par.find_all("div", recursive=False):
        # 광고/스타일/스크립트 등은 제외
        if div.attrs.get("class") in [["center_img"]]:
            continue
        # 텍스트가 있는 div만 추출
        text = div.get_text(strip=True)
        if text:
            paragraphs.append(text)

    # 빈 줄 제거 및 본문 조립
    clean_text = "\n".join([p for p in paragraphs if p.strip()])
    return clean_text.strip()
