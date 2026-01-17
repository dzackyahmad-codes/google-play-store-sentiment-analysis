# run_app.py
import os
import sys
import threading
import webbrowser
import uvicorn

def main():
    # 🔥 FIX UTAMA: inject ROOT PROJECT ke sys.path
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, BASE_DIR)

    # sekarang import aman
    from api.main import app

    def run_server():
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            log_level="warning"
        )

    threading.Thread(target=run_server, daemon=True).start()

    webbrowser.open("http://127.0.0.1:8000/app")

    input("SentimentAI running... Press ENTER to exit\n")

if __name__ == "__main__":
    main()
