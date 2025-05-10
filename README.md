# ChatGPT API가 이용한 뉴스 요약 및 메일 발송 서비스

---

## ✨ 프로젝트 소개

**ChatGPT API를 이용하여 뉴스 기사를 요약하고, 요약 결과를 메일로 발송하는 자동화 서비스**입니다.
(뉴스 직접 입력 또는 클롤링 → 요약 → 메일 전송)

---

## 📚 적용 디자인 패턴

| 패턴명            | 적용 위치                        | 설명                                                                 |
| :------------- | :--------------------------- | :----------------------------------------------------------------- |
| **추사 패턴**      | 다양한 요약 방법 제공 (GPT, TextRank) | - 요약 생성 인터페이스 통일<br>- 방식에 따라 다른 객체 생성 구조 설계                        |
| **uc625저버 패턴** | 메일 전송 후 사용자 알림               | - 메일 전송 성공 여부를 검사하고<br>- 결과를 사용자에게 알림으로 전달                         |
| **MVC 패턴**     | Django 전체 구조화                | - Model(뉴스, 요약 결과, 사용자), View(입력/출력), Controller(API 연결, 메일 전송) 분류 |

---

## 🛠️ 시스템 아키텍쳐

```plaintext
1. 뉴스 입력 (직접 입력 or 클롤링)
    ↓
2. 뉴스 요약 (요약 팩토리를 통해 다양한 요약 지원)
    ↓
3. 메일 주소 입력
    ↓
4. 요약 결과를 메일로 전송
    ↓
5. 전송 성공 여부 알림 (uc625저버 패턴)
```

---

## 👥 팀 역할 분단 (3인 기준)

| 역할      | 달연 역할                               | 비고                 |
| :------ | :---------------------------------- | :----------------- |
| 팀장 (PM) | 프로젝트 관리, 전체 구조 설계, 발표 진행            | 발표자료 준비 주도         |
| 백업데이터 1 | 뉴스 입력/클롤링 기능 개발 + 뉴스 요약 API 연결      | 추사 패턴 구현 담당        |
| 백업데이터 2 | 메일 발송 기능 개발 + 전송 성공 알림 (uc625저버 패턴) | Django 메일 모듈 활용 예정 |

---

## 🌟 주요 기능

### 기반 기능

* 뉴스 가져오기 (직접 입력 or 클롤링)
* 입력된 뉴스 본문을 요약하여 결과 생성
* 입력한 메일 주소로 요약 결과 발송
* 전송 성공 여부를 검사하고 사용자에게 알림 표시

### 보거 기능

* 관심 키워드 또는 관심 어론사 설정
* 일/주/월 단위 주요 토피크 뉴스 참고

---

## 📂 프로젝트 디렉토리 구조 예시

```plaintext
news_summary_project/
├─ manage.py
├─ README.md
├─ requirements.txt
├─ config/
│   ├─ __init__.py
│   ├─ settings.py
│   ├─ urls.py
│   └─ wsgi.py
├─ news/
│   ├─ __init__.py
│   ├─ admin.py
│   ├─ apps.py
│   ├─ models.py
│   ├─ views.py
│   ├─ urls.py
│   ├─ forms.py
│   ├─ summary/
│   │   ├─ __init__.py
│   │   ├─ base_summary.py
│   │   ├─ gpt_summary.py
│   │   └─ textrank_summary.py
│   └─ templates/
│       └─ news/
│           ├─ news_input.html
│           └─ email_result.html
├─ mailer/
│   ├─ __init__.py
│   ├─ mail_sender.py
│   └─ observer.py
└─ static/
```

---

## 🔗 참고 레퍼런스

* [ChatGPT를 이용한 뉴스 요약](https://positive-impactor.tistory.com/626)
* [클롤링 후 뉴스 요약 (Teddylee 블로그)](https://teddylee777.github.io/python/news-article/)
* [주시 뉴스 요약 메일링 프로그램](https://myeonghak.github.io/natural%20language%20processing/NLP-주시-뉴스-요약-메일-프로그램/)
* [NLP 활용 뉴스 요약 가이드](https://study-yoon.tistory.com/227)
* [News Summary - est.ai 블로그](https://blog.est.ai/2021/06/news-summary/)

---

## 🏁 프로젝트 목표

본 프로젝트는
**12주차 중간발표** 기준으로 **최소 기능(MVP) 완성과 체계적인 시스템 구조 설계**를 목표로 진행합니다.

최종 발표에서는

* MVP 완성
* 효고 확장 방향성 (예: 사용자 마찮 추천, 요약 모델 단위화)
  을 합금적으로 제시할 예안입니다.

---

# 🚀 프로젝트 설치 및 실행 방법 (최초 구조)

* Python 3.9 이상
* Django 4.x
* OpenAI API Key 필요

(새로운 설치 결함과 .env 파일 설정 방법은 후일 최종 업데이트 예정)
