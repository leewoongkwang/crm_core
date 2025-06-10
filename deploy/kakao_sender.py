import json
import time
import atexit
import requests
import logging
import os
from pathlib import Path
import sys
from kakao_module import send_kakao_message  # ← 실제 메시지 전송 구현

# ✅ 고정 로그 저장 위치: %LOCALAPPDATA%\NHCRM\kakao_sender.log
INSTALL_DIR = Path(os.getenv("LOCALAPPDATA")) / "NHCRM"
INSTALL_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = INSTALL_DIR / "kakao_sender.log"
CONFIG_PATH = INSTALL_DIR / "config.json"

LOCK_FILE = INSTALL_DIR / "kakao_sender.lock"

try:
    logging.basicConfig(
        filename=str(LOG_FILE),
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        force=True
    )
except Exception as e:
    with open("log_fallback.txt", "w") as f:
        f.write(f"❌ logging 초기화 실패: {str(e)}")

def is_already_running():
    if LOCK_FILE.exists():
        logging.warning("⚠️ 락 파일 존재 - 중복 실행 간주")
        return True
    try:
        with open(LOCK_FILE, "w") as f:
            f.write(str(os.getpid()))
        return False
    except Exception as e:
        logging.warning(f"락파일 생성 실패: {e}")
        return True

def cleanup():
    try:
        if LOCK_FILE.exists():
            LOCK_FILE.unlink()
            logging.info("✅ 락파일 삭제 완료")
    except Exception as e:
        logging.warning(f"락파일 삭제 실패: {e}")

def load_config():
    logging.info("📌 load_config() 진입")
    if not CONFIG_PATH.exists():
        logging.error("config.json 없음 - 실행 종료")
        return None
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            logging.info("✅ config.json 로드 성공")
            return json.load(f)
    except Exception as e:
        logging.exception(f"config.json 로드 실패: {e}")
        return None

def fetch_messages(host, user_id):
    try:
        url = f"http://{host}/message/api/message/lock/"
        res = requests.post(url, json={"user_id": user_id, "limit": 5}, timeout=5)
        result = res.json()

        if isinstance(result, list):
            return result
        else:
            logging.warning(f"메시지 응답이 list가 아닙: {result}")
            return []

    except Exception as e:
        logging.warning(f"메시지 불러오기 실패: {e}")
        return []

def notify_started(host, user_id):
    try:
        ping_url = f"http://{host}/message/sender-ping?user_id={user_id}&status=running"
        requests.get(ping_url, timeout=3)
        logging.info("✅ 서버에 실행 상태 ping 전송 완료")
    except Exception as e:
        logging.warning(f"❌ ping 전송 실패: {e}")

def report_status(host, msg_id, recipient_name, customer_id, status, step_log=None):
    try:
        url = f"http://{host}/message/api/message/report/"
        payload = {
            "id": msg_id,
            "recipient_name": recipient_name,
            "customer_id": customer_id,
            "status": status,
            "step_log": step_log or []
        }
        res = requests.post(url, json=payload, timeout=3)
        return res.status_code == 200
    except Exception as e:
        logging.warning(f"상태 보고 실패: {e}")
        return False
    
def on_send_done_callback(host, msg):
    def callback(result):
        logging.info(f"📤 실시간 상태 보고: {result['name']} - {result['status']}")
        ok = report_status(
            host=host,
            msg_id=msg["id"],
            recipient_name=result["name"],
            customer_id=result.get("customer_id"),
            status=result["status"],
            step_log=result.get("step_log", [])
        )
        if ok:
            logging.info(f"✅ 상태 보고 성공: {result['name']}")
        else:
            logging.warning(f"❌ 상태 보고 실패: {result['name']}")
    return callback
    
def should_shutdown(host, user_id):
    try:
        url = f"http://{host}/message/api/sender-shutdown?user_id={user_id}"
        res = requests.get(url, timeout=3)
        return res.json().get("shutdown") is True
    except Exception as e:
        logging.warning(f"❌ 종료 플래그 확인 실패: {e}")
        return False
def main():
    logging.info("⚙️ main() 진입 확인")

    try:
        config = load_config()
        if not config:
            return

        user_id = config.get("user_id")
        host = config.get("host")

        if not user_id or not host:
            logging.error("❌ config 값 부족됨: user_id 또는 host")
            return

        logging.info(f"🟢 메시지 통신 시작: {host} (user_id={user_id})")

        MAX_RETRIES = 10
        retry_count = 0

        while retry_count < MAX_RETRIES:
            messages = fetch_messages(host, user_id)

            if not messages:
                retry_count += 1
                logging.info(f"🔁 메시지 없음, {retry_count}/{MAX_RETRIES} 재시도 대기...")
                time.sleep(1.5)
                continue

            retry_count = 0  # 메시지 도착 → 초기화

            for msg in messages:
                if not isinstance(msg, dict):
                    logging.warning(f"비정상 메시지 객체: {msg}")
                    continue

                recipients = [
                    {"id": r["customer_id"], "name": r["name"]}
                    for r in msg.get("recipients", [])
                ]                
                if not all(isinstance(r, dict) and "id" in r and "name" in r for r in recipients):
                    logging.error(f"❌ recipients 포맷 오류: {recipients}")
                    continue

                logging.info(f"📨 {[r['name'] for r in recipients]}에게 메시지 전송 시도")

                results = send_kakao_message(
                    recipients=recipients,
                    message=msg.get("message", ""),
                    image_paths=[msg["image_url"]] if msg.get("image_url") else [],
                    on_send_done=on_send_done_callback(host, msg)
                )
            notify_started(host, user_id)

        logging.info("⏹ 메시지 없음 상태가 지속됨 → sender 종료")

    except Exception as e:
        logging.exception(f"❌ main() 루프 중 예외 발생: {e}")


def on_send_done_callback(host, msg):
    def callback(result):
        logging.info(f"📤 실시간 상태 보고: {result['name']} - {result['status']}")
        ok = report_status(
            host=host,
            msg_id=msg["id"],
            recipient_name=result["name"],
            customer_id=result.get("customer_id"),
            status=result["status"],
            step_log=result.get("step_log", [])
        )
        if ok:
            logging.info(f"✅ 상태 보고 성공: {result['name']}")
        else:
            logging.warning(f"❌ 상태 보고 실패: {result['name']}")
    return callback


if __name__ == "__main__":
    atexit.register(cleanup)
    if is_already_running():
        logging.info("❌ 중복 실행 감지됨 - 종료")
        sys.exit(0)
    logging.info("✅ 중복 실행 아니면, main() 호출 예정")
    main()
