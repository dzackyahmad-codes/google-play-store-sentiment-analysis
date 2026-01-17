import os
import sys
import threading
import time
import uvicorn
import webview

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)
sys.path.insert(0, BASE_DIR)

def start_api():
    uvicorn.run(
        "api.main:app",
        host="127.0.0.1",
        port=8000,
        log_level="warning"
    )

if __name__ == "__main__":
    threading.Thread(target=start_api, daemon=True).start()

    # ⏳ kasih waktu FastAPI siap
    time.sleep(3)

    webview.create_window(
        title="Sentiment Analysis Platform",
        url="http://127.0.0.1:8000/app",
        width=1200,
        height=800
    )

    webview.start()
