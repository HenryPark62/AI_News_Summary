# 📰News.ai: LLM을 활용한 뉴스 요약 및 메일 발송 서비스 <br>

## ✨ 프로젝트 소개


**LLM(OpenAI API 등)을 활용하여 뉴스 기사를 요약하고, 요약 결과를 메일로 발송하는 자동화 서비스**입니다.<br>
(뉴스 직접 입력 또는 크롤링 → 요약 → 메일 전송)
<br>

---

## 📚 적용 디자인 패턴

| 디자인 패턴                             | 적용 위치                           | 기대 효과                                                     |
| :--------------------------------- | :------------------------------ | :-------------------------------------------------------- |
| **추상 팩토리 패턴** (Abstract Factory)   | 뉴스 요약 생성기 (GPT 요약, TextRank 요약) | 다양한 요약 알고리즘을 선택적으로 적용 가능<br>요약 방식 변경 시 코드 수정 최소화          |
| **옵저버 패턴** (Observer)              | 메일 전송 성공/실패 알림 처리               | 메일 전송 결과를 이벤트 기반으로 사용자에게 전달<br>발송 로직과 알림 로직을 분리           |
| **MVC 패턴** (Model-View-Controller) | 웹 구조화 (HTML, CSS)             | Model, View, Controller 분리<br>유지보수성과 확장성 향상  |
| **전략 패턴** (Strategy)               | 뉴스 요약 방식 선택 처리                  | 실행 시점에 다양한 요약 모델(GPT, TextRank 등)을 선택 가능<br>요약 모델 교체 용이 |
| **프록시 패턴** (Proxy)                 | 외부 API(OpenAI API) 호출 최적화       | API 호출 전에 요청 제한, 캐싱 등 부가기능 추가<br>API 부하 감소                |
| **템플릿 메서드 패턴** (Template Method)   | 뉴스 크롤링 프로세스 기본 구조 설계            | 기본 크롤링 로직은 고정하고, 사이트별 차이만 하위 클래스에서 구현<br>다양한 언론사 대응 가능    |

---


## 🛠️ 시스템 아키텍처

```plaintext
1. 뉴스 입력 (직접 입력 or 크롤링)
    ↓
2. 뉴스 요약 (OpenAI API, LLM 모델 등을 활용, 요약 팩토리를 통해 다양한 요약 지원)
    ↓
3. 메일 주소 입력
    ↓
4. 요약 결과를 메일로 전송
    ↓
5. 전송 성공 여부 알림 (옵저버 패턴)
```

--- 

<br>

## 👥 팀 역할 분담

| 역할        | 담당 업무                           | 비고                 |
| :-------- | :------------------------------ | :----------------- |
| 박우진 (PM)   | 프로젝트 관리, 전체 구조 설계, 뉴스 요약 API 연결 및 프롬프트 리팩토링, 웹 페이지 개발 | AI 모듈 구현 및 연결 담당, 발표자료 준비 |
| 이선기 | 뉴스 입력/크롤링 기능 개발 | 추상 팩토리 패턴 구현 담당, 발표자료 준비    |
| 엄이슬 | 메일 발송 기능 개발 + 전송 성공 알림 (옵저버 패턴) | Django 메일 모듈 활용 예정, 발표자료 준비 |

---

## 🎯 주요 기능

### 기본 기능

* 뉴스 가져오기 (직접 입력 or 크롤링)
* 입력된 뉴스 본문을 요약하여 결과 생성
* 입력한 메일 주소로 요약 결과 발송
* 전송 성공 여부를 검사하고 사용자에게 알림 표시

### 부가 기능

* 관심 키워드 또는 관심 언론사 설정
* 일/주/월 단위 주요 토픽 뉴스 추천
* 오늘의 뉴스 (뉴스 헤드라인 - 제목 누르면 해당 뉴스 웹 페이지로 이동) 

---

## 플로우차트

---

### UI 플로우

## 4. UI 플로우

```mermaid
flowchart TB
    A[메인화면] --> B[모델 선택 + 요약 스타일 선택]
    B --> C[뉴스 입력 파일 업로드 or 텍스트 입력]
    C --> D[요약 시작 요청]
    D --> E[LLM 요약 수행]
    E --> F[요약 결과 출력 + 압축률 그래프 표시]
    F -.-> G1[요약 파일 다운로드 .txt]
    F -.-> G2[메인화면으로 돌아가기]
    F -.-> G3[요약 결과 이메일 발송]
    
```

## 5. 시스템 구조도 (Backend API 흐름)

```mermaid
flowchart TD
    A1[Frontend HTML CSS JS] --> B2[Flask Server 요청 start summary]
    B2 --> C3[Summarizer 처리]
    C3 --> D4[LLM API 호출 OpenAI Together Local]
    D4 --> E5[LLM 요약 결과 Summarizer로 반환]
    E5 --> F6[Summarizer 결과 서버로 반환]
    F6 --> G7[결과 페이지 렌더링 요약 결과와 압축률 그래프]
    G7 --> H8[이메일 발송 요청]
    H8 --> I9[Gmail SMTP 서버로 메일 발송]
```

---

## 📂 프로젝트 디렉토리 구조 (예시)

```plaintext
news_summary_project/
├── manage.py
├── README.md
├── requirements.txt
├── config/                        # Django 설정 폴더
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── news/                           # 뉴스 관련 기능 앱
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py                   # 뉴스 및 요약 결과 저장
│   ├── views.py                    # 입력/출력 처리
│   ├── urls.py
│   ├── forms.py
│   ├── summary/                    # 요약 팩토리 + 요약기 구현
│   │   ├── __init__.py
│   │   ├── base_summary.py         # SummaryGenerator 추상 클래스
│   │   ├── gpt_summary.py          # OpenAI API 기반 요약
│   │   ├── textrank_summary.py     # TextRank 기반 요약
│   │   └── else_summary.py         # 다른 모델 기반 요약
│   └── templates/
│       └── news/
│           ├── news_input.html     # 뉴스 입력 폼
│           └── email_result.html   # 메일 발송 결과 화면
├── mailer/                          # 메일 발송 및 옵저버 패턴 구현
│   ├── __init__.py
│   ├── mail_sender.py               # 메일 발송 클래스
│   └── observer.py                  # 옵저버 패턴 알림 처리
└── static/                          # 정적 파일 (css, js)
```

---

## 🏁 프로젝트 목표

**12주차 중간발표 (5/22)** 기준으로 **최소 기능(MVP) 완성과 체계적인 시스템 구조 설계**를 목표로 합니다.

최종 발표에서는

* MVP 기능 완성
* 향후 확장 방향성 (예: 사용자 맞춤형 뉴스 추천, 다양한 요약 모델 적용)
  을 함께 제시할 예정입니다.

---

## 🔗 레퍼런스

* [ChatGPT를 이용한 뉴스 요약](https://positive-impactor.tistory.com/626)
* [크롤링 후 뉴스 요약 (Teddylee 블로그)](https://teddylee777.github.io/python/news-article/)
* [주식 뉴스 요약 메일링 프로그램](https://myeonghak.github.io/natural%20language%20processing/NLP-주식-뉴스-요약-메일링-프로그램/)
* [NLP 활용 뉴스 요약 가이드](https://study-yoon.tistory.com/227)
* [News Summary - est.ai 블로그](https://blog.est.ai/2021/06/news-summary/)

