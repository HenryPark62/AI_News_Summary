# app.py (정리된 버전)
from flask import Flask, request, render_template, send_file, redirect, url_for, jsonify
import os
import smtplib

from datetime import datetime
from summarizer.summarizer import summarize_news  # 전략 기반 요약기 사용
from extractors.news_parser_naver import NaverNewsExtractor
from extractors.news_parser_newdaily import NewDailyNewsExtractor
from dotenv import load_dotenv
from mail.message import SummarizerSubject, EmailObserver # 메일보내기

load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
OUTPUT_FOLDER = './output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

progress = {"percentage": 0}

# 템플릿 메서드 기반 뉴스 파서 매핑

def extract_news_by_source(url, source):
    if source == "naver":
        return NaverNewsExtractor().extract(url)
    elif source == "newdaily":
        return NewDailyNewsExtractor().extract(url)
    elif source == "news2":
        return "뉴스2 파서 미구현"
    else:
        return "지원하지 않는 언론사입니다."

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/start-summary', methods=['POST'])
def start_summary():
    selected_model = request.form.get('model')
    selected_style = request.form.get('style')

    uploaded_file = request.files.get('file')
    input_text = request.form.get('text_content')
    input_url = request.form.get('news_url')
    news_source = request.form.get('news_source')

    news_text = ""

    if uploaded_file and uploaded_file.filename.endswith('.txt'):
        path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(path)
        with open(path, 'r', encoding='utf-8') as f:
            news_text = f.read().strip()
    elif input_text and input_text.strip():
        news_text = input_text.strip()
    elif input_url and news_source:
        news_text = extract_news_by_source(input_url.strip(), news_source.strip())
        if news_text.startswith("❌"):
            return f"본문 추출 실패: {news_text}", 400
    else:
        return "파일, 텍스트, URL 중 하나는 입력해야 합니다.", 400

    return start_summarization(news_text, selected_model, selected_style)

def start_summarization(news_text, selected_model, selected_style):
    import time
    progress["percentage"] = 0
    for i in range(5):
        progress["percentage"] += 10
        time.sleep(0.2)

    summary = summarize_news(news_text, selected_model, selected_style)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    save_path = os.path.join(OUTPUT_FOLDER, f'summary_{timestamp}.txt')
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(summary)

    progress.update({
        "percentage": 100,
        "summary": summary,
        "original_text": news_text,
        "summary_file": save_path,
        "original_length": len(news_text),
        "summary_length": len(summary)
    })

    return redirect(url_for('result'))

@app.route('/progress')
def get_progress():
    return jsonify(progress)

@app.route('/result')
def result():
    if "summary" in progress:
        return render_template(
            'result.html',
            summary_result=progress["summary"],
            original_length=progress["original_length"],
            summary_length=progress["summary_length"]
        )
    return "요약 결과가 없습니다.", 404

@app.route('/download-summary')
def download_summary():
    if "summary_file" in progress:
        return send_file(progress["summary_file"], as_attachment=True)
    return "요약 결과가 없습니다.", 404

@app.route('/send-email', methods=['POST'])
def send_email_route():
    print(f"Request form: {request.form}")
    receiver_email = request.form.get('email')
    if not receiver_email:
        print("이메일 주소 누락")
        return render_template('result.html', error="이메일 주소가 필요합니다."), 400

    try:
        if "summary_file" not in progress:
            print("요약 파일 없음")
            return render_template('result.html', error="요약 결과가 없습니다."), 404
        output_path = progress["summary_file"]
        summary = progress["summary"]

        # 옵저버 패턴으로 이메일 발송
        summarizer_subject = SummarizerSubject()  # 새 인스턴스 생성
        email_observer = EmailObserver(receiver_email)
        summarizer_subject.attach(email_observer)
        summarizer_subject.notify(summary, output_path)
        summarizer_subject.detach(email_observer)

        return redirect(url_for('result', message="이메일 발송 성공"))

    except Exception as e:
        print(f"[send_email_route] 오류: {str(e)}")
        return render_template('result.html', error=f"이메일 발송 실패: {str(e)}"), 500

if __name__ == '__main__':
    app.run(debug=True)
