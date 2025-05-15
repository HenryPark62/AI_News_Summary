# summarizer/summarizer_strategy.py

class SummarizerStrategy:
    def summarize(self, text, style):
        """
        SummarizerStrategy 기본 인터페이스
        모든 요약 클래스는 이 메서드를 오버라이드 해야 합니다.
        
        :param text: 요약할 뉴스 본문 텍스트
        :param style: 요약 스타일 ("brief" 또는 "detailed")
        :return: 요약 결과 텍스트
        """
        raise NotImplementedError("summarize() 메서드는 반드시 하위 클래스에서 구현해야 합니다.")