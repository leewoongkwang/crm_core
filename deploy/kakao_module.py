import time
import logging
from typing import List
from pywinauto import Application, Desktop
import pyperclip
import pyautogui
from pathlib import Path
from pywinauto.keyboard import send_keys

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')

FRIEND_TAB_REL_X = 30
FRIEND_TAB_REL_Y = 50

SEARCH_EDIT_ID = "100"
CHAT_EDIT_ID = "1006"
ATTACH_BUTTON_ID = "AttachmentButton"
OPEN_DIALOG_TITLE = "열기"
FILE_EDIT_ID = "1148"

def prepare_kakao_window():
    try:
        app = Application(backend="uia").connect(path="KakaoTalk.exe")
        main = app.window(title_re="카카오톡")
        main.set_focus()
        success = click_friend_tab_safely(main)
        if not success:
            raise RuntimeError("❌ 친구탭 클릭 실패")
        return app, main
    except Exception as e:
        logging.exception("카카오톡 초기화 실패")
        raise

def click_friend_tab_safely(main_window, max_attempts=3) -> bool:
    rect = main_window.rectangle()
    abs_x, abs_y = rect.left + FRIEND_TAB_REL_X, rect.top + FRIEND_TAB_REL_Y

    for attempt in range(1, max_attempts + 1):
        logging.info(f"[{attempt}] 친구탭 클릭 시도 중...")
        pyautogui.moveTo(abs_x, abs_y, duration=0.2)
        pyautogui.click()
        time.sleep(0.6)
        if is_friend_tab_active(main_window):
            logging.info("✅ 친구탭 클릭 성공")
            return True
        logging.warning("친구탭 클릭 실패, fallback 시도...")
        pyautogui.moveTo(abs_x + 10, abs_y + 10, duration=0.2)
        pyautogui.click()
        time.sleep(0.5)
        if is_friend_tab_active(main_window):
            logging.info("✅ fallback 클릭 성공")
            return True
    logging.error("❌ 친구탭 클릭 완전 실패")
    return False

def is_friend_tab_active(main_window) -> bool:
    try:
        pane = main_window.child_window(auto_id="1149", control_type="Pane")
        return pane.exists(timeout=1)
    except Exception as e:
        logging.debug(f"친구탭 active 확인 중 예외: {e}")
        return False

def send_kakao_message(recipients, message: str, image_paths: List[str] = None, retry: int = 2, on_send_done=None) -> List[dict]:
    image_paths = image_paths or []
    if isinstance(recipients, str):
        recipients = [recipients]

    results = []
    try:
        app, main = prepare_kakao_window()
    except Exception as e:
        for rec in recipients:
            name = rec["name"]
            results.append({
                "name": name,
                "customer_id": rec["id"],
                "status": "failed",
                "step_log": [{"step": "prepare_kakao", "result": "fail", "reason": str(e)}]
            })
        return results

    for i, rec in enumerate(recipients, 1):
        name = rec["name"]
        cid = rec["id"]

        logging.info(f"[{i}] {name} (ID={cid})에게 메시지 전송 중...")
        result = send_to_one(app, main, name, message, image_paths, retry)
        result["name"] = name
        result["customer_id"] = cid

        # ✅ 콜백 실행
        if on_send_done:
            try:
                on_send_done(result)
            except Exception as e:
                logging.warning(f"❌ on_send_done 콜백 예외: {e}")

        results.append(result)
        time.sleep(1.0)

    return results

def send_to_one(app, main, contact_name, message, image_paths, retry) -> dict:
    step_log = []
    for attempt in range(1, retry + 1):
        try:
            try:
                send_keys("^f", with_spaces=True)
                time.sleep(0.3)
                search_edit = main.child_window(auto_id=SEARCH_EDIT_ID, control_type="Edit")
                search_edit.set_focus()
                search_edit.set_edit_text(contact_name)
                send_keys("{ENTER}", with_spaces=True)
                time.sleep(0.3)
                step_log.append({"step": "search_contact", "result": "ok"})
            except Exception as e:
                step_log.append({"step": "search_contact", "result": "fail", "reason": str(e)})
                continue

            try:
                chat_win = next((w for w in Desktop(backend="uia").windows() if contact_name in w.window_text()), None)
                if not chat_win:
                    raise Exception("채팅창 탐색 실패")
                step_log.append({"step": "open_chat", "result": "ok"})
            except Exception as e:
                step_log.append({"step": "open_chat", "result": "fail", "reason": str(e)})
                continue

            try:
                chat_edit = next((ctrl for ctrl in chat_win.descendants(control_type="Document") if ctrl.automation_id() == CHAT_EDIT_ID), None)
                pyperclip.copy(message)
                chat_edit.set_focus()
                chat_edit.click_input()
                time.sleep(0.1)
                send_keys("^v", with_spaces=True, pause=0.05)
                step_log.append({"step": "send_message", "result": "ok"})
            except Exception as e:
                step_log.append({"step": "send_message", "result": "fail", "reason": str(e)})
                continue

            try:
                for img in image_paths:
                    attach_btn = main.child_window(auto_id=ATTACH_BUTTON_ID, control_type="Button")
                    attach_btn.click_input()
                    time.sleep(0.3)
                    dlg = app.window(title_re=OPEN_DIALOG_TITLE)
                    file_edit = dlg.child_window(auto_id=FILE_EDIT_ID, control_type="Edit")
                    file_edit.wait("ready", timeout=2)
                    file_edit.set_edit_text(str(img))
                    dlg.child_window(title="열기", control_type="Button").click_input()
                    thumb = main.child_window(control_type="Image", title_re=f".*{Path(img).name}.*")
                    thumb.wait("visible", timeout=3)
                    time.sleep(0.2)
                if image_paths:
                    step_log.append({"step": "send_image", "result": "ok"})
            except Exception as e:
                step_log.append({"step": "send_image", "result": "fail", "reason": str(e)})
                continue

            try:
                send_keys("{ENTER}", with_spaces=True)
                send_keys("{ESC}", with_spaces=True)
                step_log.append({"step": "confirm_enter", "result": "ok"})
                return {"status": "sent", "step_log": step_log}
            except Exception as e:
                step_log.append({"step": "confirm_enter", "result": "fail", "reason": str(e)})
                continue
        except Exception as e:
            step_log.append({"step": "unexpected", "result": "fail", "reason": str(e)})
            continue

    return {"status": "failed", "step_log": step_log}
