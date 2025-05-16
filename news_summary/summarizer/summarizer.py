from .perplexity_summarizer import PerplexitySummarizer
from .together_summarizer import TogetherSummarizer
from .local_summarizer import LocalSummarizer

# =====================
# Summarizer 전략 선택
# =====================

def get_summarizer(model_name):
    if model_name == "perplexity":
        return PerplexitySummarizer()
    elif model_name == "together":
        return TogetherSummarizer()
    elif model_name == "local":
        return LocalSummarizer()
    else:
        return PerplexitySummarizer()  # 기본값

# =====================
# 프롬프트 생성 함수
# =====================

def create_prompt(text, style):
    if style == "brief":
        return (
            "다음은 뉴스 기사 전문입니다.\n\n"
            f"{text}\n\n"
            "이 뉴스를 한국어로 간결하고 핵심만 요약해 주세요. (2~3줄 이내)"
        )
    elif style == "detailed":
        return (
            "다음은 뉴스 기사 전문입니다.\n\n"
            f"{text}\n\n"
            "이 뉴스를 한국어로 상세하고 풍부하게 요약해 주세요. (5~7줄 정도)"
        )
    else:
        return (
            "다음은 뉴스 기사 전문입니다.\n\n"
            f"{text}\n\n"
            "이 뉴스를 한국어로 간결하고 명확하게 3~5줄 이내로 요약해 주세요."
        )

# =====================
# 메인 요약 함수
# =====================

def summarize_news(text, model_name="openai", style="brief"):
    summarizer = get_summarizer(model_name)
    return summarizer.summarize(text, style)