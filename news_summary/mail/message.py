# send.py
from abc import ABC, abstractmethod
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from dotenv import load_dotenv

load_dotenv()

# 옵저버 인터페이스
class Observer(ABC):
    @abstractmethod
    def update(self, summary: str, output_file: str):
        pass

# 이메일 발송 옵저버
class EmailObserver(Observer):
    def __init__(self, email: str):
        self.email = email
        self.gmail_user = os.getenv("GMAIL_USER")
        self.gmail_app_password = os.getenv("GMAIL_APP_PASSWORD")
        if not self.gmail_user or not self.gmail_app_password:
            raise ValueError("GMAIL_USER or GMAIL_APP_PASSWORD not set")

    def update(self, summary: str, output_file: str):
        # 이메일 구성
        msg = MIMEMultipart()
        msg['Subject'] = '[뉴스 요약 서비스] 요약본을 보내드립니다.'
        msg['From'] = self.gmail_user
        msg['To'] = self.email

        # 본문
        body = f"안녕하세요, 요청하신 뉴스 요약본을 보내드립니다.\n요약 내용:\n{summary}"
        msg.attach(MIMEText(body, 'plain', 'utf-8'))

        # 첨부파일
        with open(output_file, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename={os.path.basename(output_file)}'
        )
        msg.attach(part)

        # Gmail SMTP로 발송
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(self.gmail_user, self.gmail_app_password)
                server.sendmail(self.gmail_user, self.email, msg.as_string())
            print(f"[EmailObserver] 이메일 발송 성공: {self.email}")
        except Exception as e:
            print(f"[EmailObserver] 이메일 발송 실패: {str(e)}")
            raise

# 주체 클래스
class SummarizerSubject:
    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, summary: str, output_file: str):
        for observer in self._observers:
            observer.update(summary, output_file)
