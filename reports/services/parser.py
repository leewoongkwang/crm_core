# reports/services/parser.py

import fitz  # PyMuPDF
import pdfplumber
import re
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

def pdf_to_json(pdf_path: str) -> Dict[str, Any]:
    customer: Dict[str, Any] = {}
    coverage: List[Dict[str, Any]] = []
    insurance_overview: List[Dict[str, Any]] = []

    # ------------------------
    # 1. 고객 정보 추출
    # ------------------------
    try:
        with fitz.open(pdf_path) as doc:
            text2 = doc.load_page(1).get_text().strip()
        lines = [line.strip() for line in text2.splitlines() if line.strip()]

        contract_count = int(lines[0].replace('건', '')) if lines else None
        monthly_premium = lines[1] if len(lines) > 1 else None

        name = None
        if len(lines) > 3 and '고객님' in lines[3]:
            m = re.search(r"(\S+?)\s+고객님", lines[3])
            name = m.group(1) if m else None

        gender, age = None, None
        if len(lines) > 4:
            ga = lines[4]
            gm = re.search(r"(\S+?)/보험나이", ga)
            am = re.search(r"/보험나이\s*(\d+)세", ga)
            gender = gm.group(1) if gm else None
            age = int(am.group(1)) if am else None

        sangryeong = None
        if len(lines) > 5 and ':' in lines[5]:
            sangryeong = lines[5].split(':', 1)[1].strip()

        customer = {
            '이름': name,
            '성별': gender,
            '나이': age,
            '상령일': sangryeong,
            '정상계약_개수': contract_count,
            '월납입보험료': monthly_premium
        }

    except Exception as e:
        logger.exception("고객 정보 파싱 오류")
        customer = {
            '이름': None, '성별': None, '나이': None,
            '상령일': None, '정상계약_개수': None, '월납입보험료': None
        }

    # ------------------------
    # 2. 보장 항목 추출
    # ------------------------
    try:
        with fitz.open(pdf_path) as doc:
            pages = [i for i in range(doc.page_count)
                     if '전체 보장현황' in doc.load_page(i).get_text()]

        with pdfplumber.open(pdf_path) as pdf:
            for idx in pages:
                page = pdf.pages[idx]
                tables = page.extract_tables()
                for table in tables:
                    header = table[0]
                    if '담보명' in header and '가입금액' in header:
                        col_idx = {col: i for i, col in enumerate(header)}
                        for row in table[1:]:
                            cov_name = row[col_idx['담보명']]
                            cov_amt = row[col_idx['가입금액']]
                            if cov_name and cov_amt:
                                coverage.append({
                                    'coverage_name': cov_name.strip(),
                                    'coverage_amount': cov_amt.strip()
                                })
                        break

    except Exception as e:
        logger.exception("보장 항목 파싱 오류")
        coverage = []

    # ------------------------
    # 3. 보험상품 요약 추출
    # ------------------------
    try:
        with fitz.open(pdf_path) as doc:
            pages = [i for i in range(doc.page_count)
                     if '가입보험 전체현황' in doc.load_page(i).get_text()]

        with pdfplumber.open(pdf_path) as pdf:
            for idx in pages:
                page = pdf.pages[idx]
                tables = page.extract_tables()
                for table in tables:
                    header = table[0]
                    if '보험회사명' in header:
                        if len(table) > 2 and table[1][0] == '보험상품명':
                            product_row = table[2]
                            start_row = 3
                        else:
                            product_row = table[1]
                            start_row = 2

                        for j in range(2, len(header)):
                            rec: Dict[str, Any] = {
                                '보험회사명': header[j],
                                '상품명': product_row[j] if j < len(product_row) else None
                            }
                            for i in range(start_row, len(table)):
                                label = table[i][1]
                                if label:
                                    value = table[i][j] if j < len(table[i]) else None
                                    if value and value.strip():
                                        rec[label] = value.strip()
                            if any(v for k, v in rec.items() if k not in ('보험회사명', '상품명')):
                                insurance_overview.append(rec)
                        break

    except Exception as e:
        logger.exception("보험상품 요약 파싱 오류")
        insurance_overview = []

    # ------------------------
    # 최종 결과 반환
    # ------------------------
    return {
        'customer': customer,
        'coverage': coverage,
        'insurance_overview': insurance_overview
    }
