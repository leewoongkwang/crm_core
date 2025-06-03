# 🗺️ CRM 프로젝트 ROUTER_MAP (v2 - 앱 리팩토링 이후)

---

## ✅ 홈 / 대시보드

| URL 경로 | 메서드 | 설명 | 템플릿 | View |
|----------|--------|------|--------|------|
| `/home/` | GET | KPI 요약, 터치고객, 계약 및 활동 차트 | `home.html` | `home.views.home_view` |

---

## ✅ 고객(Customer)

| URL 경로 | 메서드 | 설명 | 템플릿 | View |
|----------|--------|------|--------|------|
| `/customer/list/` | GET | 고객 목록 조회 (검색/필터링) | `customers/list.html` | `customers.views.customer_list` |
| `/customer/<id>/` | GET | 고객 상세 보기 (탭포함) | `customers/detail.html` | `customers.views.customer_detail` |

---

## ✅ 14터치(TouchLog)

| URL 경로 | 메서드 | 설명 | 템플릿 | View |
|----------|--------|------|--------|------|
| `/touch/?ids=1,2,3` | GET | 14터치 메시지 입력화면 | `touchlog/form.html` | `touchlog.views.touch_form` |
| `/touch/send/` | POST | 메시지 전송 + TouchLog 생성 | 없음 (redirect 또는 ajax 응답) | `touchlog.views.send_message` |

---

## ✅ 리포트 분석

| URL 경로 | 메서드 | 설명 | 템플릿 | View |
|----------|--------|------|--------|------|
| `/analysis/<report_id>/` | GET | 보장분석 (리포트 상세 파싱 시각화) | `analysis/detail.html` | `analysis.views.report_analysis` |
| `/analysis/?customer_id=5` | GET | 최신 리포트 기준 분석 | `analysis/detail.html` | `analysis.views.analysis_by_customer` |

---

## ✅ 영업전략(Strategy)

| URL 경로 | 메서드 | 설명 | 템플릿 | View |
|----------|--------|------|--------|------|
| `/strategy/` | GET | 이번 달 전략 조회 | `strategy/form.html` | `strategy.views.view_strategy` |
| `/strategy/` | POST | 전략 저장/수정 | 없음 (POST 처리) | `strategy.views.save_strategy` |

---

## ✅ 실적입력 / 해야할일(Task/KPI)

| URL 경로 | 메서드 | 설명 | 템플릿 | View |
|----------|--------|------|--------|------|
| `/tasks/` | GET | 오늘 실적 현황 + KPI 비교 | `activity/tasks.html` | `activity.views.task_dashboard` |
| `/tasks/submit/` | POST | 오늘 실적 입력/수정 | 없음 | `activity.views.task_submit` |

---

## ✅ 로그인/계정

| URL 경로 | 메서드 | 설명 | 템플릿 | View |
|----------|--------|------|--------|------|
| `/login/` | GET/POST | 로그인 화면 + 처리 | `accounts/login.html` | `accounts.views.login_view` |
| `/logout/` | GET | 로그아웃 후 리디렉션 | 없음 | `accounts.views.logout_view` |

---

## 🛠️ 추가 예정 API (관리자/통계 등)

| URL 경로 | 메서드 | 설명 | 템플릿/응답 | View |
|----------|--------|------|-------------|------|
| `/api/tasks/kpi-summary/` | GET | KPI 비교 결과 JSON | JSON | `activity.api.kpi_summary` |
| `/api/touchlog/recent/` | GET | 최근 터치 이력 리스트 | JSON | `touchlog.api.recent_logs` |

---

## 🔒 Notes

- 모든 고객/리포트/터치 요청은 `request.user.id` 기준으로 접근 제한
- `@login_required` 기본 적용
- 템플릿은 Django 기본 template loader 기준 app별 디렉토리에 위치

