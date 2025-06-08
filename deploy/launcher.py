import os
import sys
import urllib.request
import subprocess
import json
from pathlib import Path

# 실행파일 설정
EXE_NAME = "kakao_sender.exe"
CONFIG_NAME = "config.json"
DOWNLOAD_URL = "http://43.201.73.219:8000//download/kakao_sender.exe"  # ✅ 고정 다운로드 링크

def ensure_exe_exists(exe_path):
    if not exe_path.exists():
        print("📦 본체 실행 파일이 없습니다. 자동 다운로드 중...")
        try:
            urllib.request.urlretrieve(DOWNLOAD_URL, exe_path)
            print("✅ 다운로드 완료")
        except Exception as e:
            print(f"❌ 다운로드 실패: {e}")
            sys.exit(1)

def create_config(config_path, user_id, host):
    config = {
        "user_id": user_id,
        "host": host
    }
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def main():
    if len(sys.argv) < 3:
        print("❌ 실행 인자 부족. 예: launcher.exe 3 crm.myserver.com")
        sys.exit(1)

    user_id = sys.argv[1]
    host = sys.argv[2]

    # 현재 디렉토리 기준 경로 설정
    base_path = Path(__file__).resolve().parent
    exe_path = base_path / EXE_NAME
    config_path = base_path / CONFIG_NAME

    # config 생성
    create_config(config_path, user_id, host)

    # 실행파일 없으면 다운로드
    ensure_exe_exists(exe_path)

    # 본체 실행
    subprocess.Popen([str(exe_path)])

if __name__ == "__main__":
    main()
