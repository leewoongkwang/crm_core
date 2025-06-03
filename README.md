# CRM Core 지향 README

개인 보험설계사를 위한 웹 기반 고객관리 시스템.
가망 고객 관리, 터치 이력, 보험 리포트 분석, KPI 통계 기반 업무 보조 도구 제공.

---

## 프로젝트 구조

```
crm_core/
├── customers/                  # 고객 관리 앱
│   ├── models.py               # 고객 정보 모델 정의
│   ├── forms.py                # CustomerForm: 등록/수정용
│   ├── views.py                # 고객 CRUD + ListView
│   ├── urls.py                 # /customer/ URL 정의
│   └── templates/customers/
│       ├── list.html           # 고객 목록
│       ├── form.html           # 등록/수정 공용 폼
│       ├── detail.html         # 고객 상세 보기
│       └── delete.html         # 삭제 확인
│
├── contracts/                  # 계약 관리 앱 (예정)
├── reports/                    # 보장 리포트 분석 앱 (예정)
├── touchlogs/                  # 14터치 기록 앱 (예정)
├── standard_activity/          # KPI 활동 기록 앱 (예정)
│
├── crm_core/                   # 프로젝트 설정
│   ├── settings.py             # AWS, DB, 인증 설정 포함
│   ├── urls.py                 # 앱별 include 구조
│
├── templates/
│   └── base.html               # 전체 공통 레이아웃
│
└── manage.py
```

---

## 기술 스택

* **Backend**: Django 5.2+
* **DB**: SQLite (개발), PostgreSQL (사용 전환 예정)
* **Frontend**: Django Template + Tailwind CSS
* **Hosting**: AWS EC2
* **Storage**: AWS S3 (PDF 리포트 등)
* **Security**: 모든 객인정보 암호화 저장 필수


## 개발 기준

| 항목    | 내용                                     |
| ----- | -------------------------------------- |
| 폴더 구조 | 앱별 `templates/앱명/파일.html` 구조 없이 지정     |
| View  | 함수형 기반, 등록/수정은 `forms.py` 기반 처리        |
| Form  | `CustomerForm` 등 ModelForm으로 관리        |
| 템플릿   | Tailwind 기반 디자인, 각 필드별 입력 제어 포함        |
| 검증    | `forms.py` 내 `clean_` 함수로 입력 유효성 보장    |
| 보안    | `CSRF`, `@login_required`, 객인정보 암호화 필수 |
| 확장성   | 모든 앱은 기능별로 분리 유지, include 방식 URL       |


## 로컬 개발 시행

# 환경 구성
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 마이그레이션 및 실행
python manage.py migrate
python manage.py runserver


##
