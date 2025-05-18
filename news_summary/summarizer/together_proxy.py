# summarizer/together_proxy.py
# Proxy: TogetherSummarizer 호출 전 인증 및 로깅 처리

import os
from .summarizer_strategy import SummarizerStrategy
from .together_summarizer import TogetherSummarizer
from .prompt_utils import create_prompt

class TogetherProxy(SummarizerStrategy):
    def __init__(self):
        self.api_key = os.getenv("TOGETHER_API_KEY", "YOUR_DEFAULT_TOGETHER_KEY")
        self.real_summarizer = TogetherSummarizer(api_key=self.api_key)

    def summarize(self, text, style):
        print(f"[TogetherProxy] 스타일: {style}, 길이: {len(text)}자 → 요약 시작")
        return self.real_summarizer.summarize(text, style)