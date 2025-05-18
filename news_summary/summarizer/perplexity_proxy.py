# summarizer/perplexity_proxy.py

# ✅ Proxy: Perplexity API 호출에 대한 대리자
import os
from .summarizer_strategy import SummarizerStrategy
from .perplexity_summarizer import PerplexitySummarizer
from .prompt_utils import create_prompt

class PerplexityProxy(SummarizerStrategy):
    def __init__(self):
        self.api_key = os.getenv("PERPLEXITY_API_KEY", "YOUR_DEFAULT_API_KEY")
        self.real_summarizer = PerplexitySummarizer(api_key=self.api_key)

    def summarize(self, text, style):
        print(f"[PerplexityProxy] 요청 시작: 스타일={style}, 길이={len(text)}자")
        return self.real_summarizer.summarize(text, style)