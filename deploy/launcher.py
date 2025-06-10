import os
import sys
import urllib.request
import subprocess
import json
from pathlib import Path
import logging

# ✅ 설치 및 로그 저장 위치: %LOCALAPPDATA%\NHCRM
try:
    INSTALL_DIR = Path(os.getenv("LOCALAPPDATA")) / "NHCRM"
    INSTALL_DIR.mkdir(parents=True, exist_ok=True)

    LOG_FILE = INSTALL_DIR / "launcher_debug.log"
    logging.basicConfig(
        filename=str(LOG_FILE),
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )
except Exception as e:
    print("❌ 로그 설정 중 오류:", e)
    sys.exit(1)

EXE_NAME = "kakao_sender.exe"
CONFIG_NAME = "config.json"
DOWNLOAD_URL = "http://3.38.7.3:8000/static/download/kakao_sender.exe"
DETACHED_PROCESS = 0x00000008
DEFAULT_HOST = "3.38.7.3:8000"


def is_already_running(process_name):
    result = subprocess.run(
        ["tasklist", "/FI", f"IMAGENAME eq {process_name}"],
        stdout=subprocess.PIPE, text=True
    )
    return process_name in result.stdout

def ensure_exe_exists(exe_path):
    if not exe_path.exists():
        logging.info("📦 kakao_sender.exe 없음 → 다운로드 시작")
        try:
            urllib.request.urlretrieve(DOWNLOAD_URL, exe_path)
            logging.info("✅ kakao_sender.exe 다운로드 완료")
        except Exception as e:
            logging.exception(f"❌ kakao_sender 다운로드 실패: {e}")
            sys.exit(1)

def create_config(config_path, user_id, host):
    try:
        config = {"user_id": user_id, "host": host}
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        logging.info("✅ config.json 생성 완료")
    except Exception as e:
        logging.exception(f"❌ config 생성 실패: {e}")
        sys.exit(1)

def main():
  
    logging.info("🚀 launcher 실행 시작")

    if is_already_running(EXE_NAME):
        logging.warning("⚠️ kakao_sender.exe 중복 실행 감지 → 종료")
        sys.exit(0)

    if len(sys.argv) < 2:
        logging.error("❌ user_id 인자가 필요합니다. 예: launcher.exe <user_id>")
        sys.exit(1)
    
    user_id, host = parse_custom_scheme(sys.argv[1])

    logging.info(f"📌 실행 인자 user_id={user_id}, host={host}")
    logging.info(f"📂 설치 경로: {INSTALL_DIR}")

    exe_path = INSTALL_DIR / EXE_NAME
    config_path = INSTALL_DIR / CONFIG_NAME

    create_config(config_path, user_id, host)
    ensure_exe_exists(exe_path)

    try:
        subprocess.Popen([str(exe_path)], creationflags=DETACHED_PROCESS)
        logging.info("✅ kakao_sender.exe 백그라운드 실행 성공")
    except Exception as e:
        logging.exception(f"❌ kakao_sender 실행 실패: {e}")

    logging.info("🔚 launcher 종료 완료")


def is_installed():
    exe_path = INSTALL_DIR / EXE_NAME
    return exe_path.exists()

def run_check_install():
    logging.info("🟡 check-install 모드 실행됨")
    if is_installed():
        logging.info("✅ 설치되어 있음 → Ping Yes / Main 진입")
        try:
            urllib.request.urlopen("http://3.38.7.3:8000/message/launcher-ping?installed=yes")
        except:
            pass
        sys.exit(0)
    else:
        logging.warning("❌ 설치 안됨 → ping 보냄 후 설치 시작")
        try:
            urllib.request.urlopen("http://3.38.7.3:8000/message/launcher-ping?installed=no")
        except:
            pass
        sys.exit(1)

def parse_custom_scheme(arg):
    if arg.startswith("nhcrm://"):
        parts = arg.replace("nhcrm://", "").split("/")
        if len(parts) == 2:
            return parts[0], parts[1]
    return None, None

if __name__ == "__main__":

    logging.info("🟢 launcher 진입 - 인자: %s", sys.argv)

    if len(sys.argv) >= 2 and "check-install" in sys.argv[1].lower():
        run_check_install()
    main()
