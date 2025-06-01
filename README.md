# CRM Core (보험설계사 전용 CRM 시스템)

개인 설계사 업무를 위한 웹 기반 CRM.  
고객관리, 실적관리, 14터치, 보장분석 리포트 등 통합 기능 제공.

## ✅ 기술 스택
- Django (백엔드, 템플릿)
- SQLite (개발용), RDS(MySQL/PostgreSQL) 대응
- AWS EC2, S3
- TailwindCSS
- PyQt5 (MVP 시뮬레이션 테스트)

## 📁 디렉토리 구조

```plaintext
crm_core/
├── manage.py
├── crm_core/       # Django 설정 (settings.py, urls.py)
├── customers/      # 고객 모델
├── dashboard/      # 뷰 모음 (home, tasks, strategy, analysis 등)
├── activity/       # DailyStandardActivity 모델
├── contracts/      # 보험 계약 관련
├── reports/        # 리포트 업로드 및 파싱
├── strategy/       # 영업 전략 수립
├── touchlog/       # 고객 접촉 기록
├── accounts/          # 사용자 모델 (설계사)
├── templates/      # 템플릿 HTML
│   ├── base.html
│   ├── customer/
│   │   ├── list.html, form.html, detail.html, delete.html
│   └── 기타: home.html, tasks.html, touch.html 등

