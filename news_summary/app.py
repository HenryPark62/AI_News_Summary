# app.py (정리된 버전)
from flask import Flask, request, render_template, send_file, redirect, url_for, jsonify, session
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
import time
import smtplib
from email.message import EmailMessage
from datetime import datetime
from summarizer.summarizer import summarize_news  # 전략 기반 요약기 사용
from extractors.news_parser_naver import NaverNewsExtractor
from extractors.news_parser_annnews import AnnNewsExtractor
from extractors.news_parser_foxnews import FoxNewsExtractor
from dotenv import load_dotenv
from news_headlines import get_latest_headlines

from mail.message import SummarizerSubject
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import google.oauth2.credentials
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import base64

load_dotenv()


app = Flask(__name__)
app.secret_key = os.urandom(24)  # 세션용 비밀 키
app.config['UPLOAD_FOLDER'] = './Uploads'
app.config['OUTPUT_FOLDER'] = './output'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

progress = {"percentage": 0}

# OAuth 2.0 설정
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.readonly'  # getProfile에 필요
]
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')

if not all([CLIENT_ID, CLIENT_SECRET, REDIRECT_URI]):

      raise ValueError("Missing OAuth credentials in .env")


# 템플릿 메서드 기반 뉴스 파서 매핑

def extract_news_by_source(url, source):
    if source == "naver":
        return NaverNewsExtractor().extract(url)
    elif source == "annnews":
        return AnnNewsExtractor().extract(url)
    elif source == "foxnews":
        return FoxNewsExtractor().extract(url)
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
        path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
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
    print(f"Starting summarization: model={selected_model}, style={selected_style}")
    progress["percentage"] = 0
    for i in range(5):
        progress["percentage"] += 10
        time.sleep(0.2)

    print("Calling summarize_news")
    summary = summarize_news(news_text, selected_model, selected_style)
    print(f"Summary result: {summary[:100]}...")
    if "API 오류" in summary:
        print(f"Summary failed: {summary}")
        return render_template('result.html', error=f"요약 실패: {summary}"), 400

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    save_path = os.path.join(app.config['OUTPUT_FOLDER'], f'summary_{timestamp}.txt')
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(summary)

    progress.update({
        "percentage": 100,
        "summary": summary,
        "original_text": news_text,
        "summary_file": save_path,
        "original_length": len(news_text),
        "summary_length": len(summary),
        "credentials": session.get('credentials')  # 추가
    })

    print("Summarization completed")
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
            summary_length=progress["summary_length"],
            message=request.args.get('message')
        )
    return render_template('result.html', error="요약 결과가 없습니다."), 404

@app.route('/download-summary')
def download_summary():
    if "summary_file" in progress:
        return send_file(progress["summary_file"], as_attachment=True)
    return "요약 결과가 없습니다.", 404

@app.route('/login')
def login():
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uris": [REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=SCOPES
    )
    flow.redirect_uri = REDIRECT_URI
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    session['state'] = state
    return redirect(authorization_url)

@app.route('/oauth2callback')
def oauth2callback():
    state = session.get('state')
    flow = Flow.from_client_config(
        {
            "web": {
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET,
                "redirect_uris": [REDIRECT_URI],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        },
        scopes=SCOPES,
        state=state
    )
    flow.redirect_uri = REDIRECT_URI
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    return redirect(url_for('result', message="Gmail 인증 성공"))

@app.route('/send-email', methods=['GET', 'POST'])
def send_email():
    # GET 요청 처리 (예: 인증 상태 확인)
    if request.method == 'GET':
        return redirect(url_for('result', message="로그인 성공"))
    
    if 'credentials' not in session:
        return redirect(url_for('login'))
    credentials = session['credentials']
    try:
        service = build('gmail', 'v1', credentials=google.oauth2.credentials.Credentials(**credentials))
        # 사용자 이메일 가져오기
        profile = service.users().getProfile(userId='me').execute()
        user_email = profile['emailAddress']
        print(f"Sending email to: {user_email}")

        # 이메일 메시지 생성
        msg = MIMEMultipart()
        msg['Subject'] = '[뉴스 요약 서비스] 요약본을 보내드립니다.'
        msg['From'] = user_email
        msg['To'] = user_email

        body = f"안녕하세요, 요청하신 뉴스 요약본을 보내드립니다.\n요약 내용:\n{progress['summary']}"
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        with open(progress['summary_file'], 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename={os.path.basename(progress["summary_file"])}'
        )
        msg.attach(part)

        # Gmail API로 이메일 전송
        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode('utf-8')
        message = {'raw': raw}
        service.users().messages().send(userId='me', body=message).execute()
        print("Email sent successfully")

        # SummarizerSubject 알림 (옵션)
        summarizer_subject = SummarizerSubject()
        summarizer_subject.notify(progress['summary'], progress['summary_file'])

        return redirect(url_for('result', message="이메일 발송 성공"))
    except HttpError as e:
        print(f"[send_email] Gmail API 오류: {str(e)}")
        return render_template('result.html', error=f"이메일 발송 실패: {str(e)}"), 500
    except Exception as e:
        print(f"[send_email] 오류: {str(e)}")
        return render_template('result.html', error=f"이메일 발송 실패: {str(e)}"), 500
        
@app.route('/api/latest-headlines')
def latest_headlines():
    headlines = get_latest_headlines()
    return jsonify({"headlines": headlines})

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/terms')
def terms():
    return render_template('terms.html')

if __name__ == '__main__':
    app.run(debug=True)
