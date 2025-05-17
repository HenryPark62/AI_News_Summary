from flask import Flask, request, render_template, send_file, redirect, url_for, jsonify
import os
import smtplib
from email.message import EmailMessage
from datetime import datetime
from summarizer import summarize_news  # 패키지화된 summarizer 사용

# 뉴스 파서들
from extractors.news_parser_naver import extract_clean_news_body as parse_naver
from extractors.news_parser_newdaily import extract_clean_news_body as parse_newdaily

# 미구현 뉴스 파서
#from news_parser.news2_parser import extract_clean_news_body as parse_news2


# 뉴스 파서 매핑 함수
def extract_news_by_source(url, source):
    if source == "naver":
        return parse_naver(url)
    elif source == "newdaily":
        return parse_newdaily(url)
    elif source == "news2":
        return "❌ 뉴스2 파서 미구현"
    else:
        return "❌ 지원하지 않는 언론사입니다."


app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
OUTPUT_FOLDER = './output'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

progress = {"percentage": 0}

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

    # 우선순위: 파일 > 텍스트 > URL
    if uploaded_file and uploaded_file.filename.endswith('.txt'):
        file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(file_path)
        with open(file_path, 'r', encoding='utf-8') as f:
            news_text = f.read().strip()
    elif input_text and input_text.strip() != "":
        news_text = input_text.strip()
    elif input_url and news_source:
        news_text = extract_news_by_source(input_url.strip(), news_source.strip())
        if news_text.startswith("❌"):
            return f"본문 추출 실패: {news_text}", 400
    else:
        return "❌ 파일, 텍스트, URL 중 하나는 입력해야 합니다.", 400

    return start_summarization(news_text, selected_model, selected_style)

def start_summarization(news_text, selected_model, selected_style):
    progress["percentage"] = 0

    import time
    for i in range(5):
        progress["percentage"] += 10
        time.sleep(0.2)

    summary = summarize_news(news_text, selected_model, selected_style)

    original_length = len(news_text)
    summary_length = len(summary)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    save_path = os.path.join(OUTPUT_FOLDER, f'summary_{timestamp}.txt')

    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(summary)

    progress["percentage"] = 100
    progress["summary"] = summary
    progress["original_text"] = news_text
    progress["original_length"] = original_length
    progress["summary_length"] = summary_length
    progress["summary_file"] = save_path

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
    else:
        return "요약 결과가 없습니다.", 404

@app.route('/download-summary')
def download_summary():
    if "summary_file" in progress:
        return send_file(progress["summary_file"], as_attachment=True)
    return "요약 결과가 없습니다.", 404

@app.route('/send-email', methods=['POST'])
def send_email_route():
    data = request.get_json()
    receiver_email = data.get('email')

    try:
        sender_email = "너의@gmail.com"  # 본인 Gmail 주소
        sender_password = "앱 비밀번호"   # 본인 Gmail 앱 비밀번호

        msg = EmailMessage()
        msg['Subject'] = '[뉴스 요약 서비스] 요약본을 보내드립니다.'
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg.set_content(f"""안녕하세요, 요청하신 뉴스 요약본을 보내드립니다.

요약 내용:
{progress.get('summary', '')}
""")

        if "summary_file" in progress:
            with open(progress["summary_file"], 'rb') as f:
                file_data = f.read()
                file_name = os.path.basename(progress["summary_file"])
                msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)

        return jsonify({"success": True})
    except Exception as e:
        print(e)
        return jsonify({"success": False})

if __name__ == '__main__':
    app.run(debug=True)