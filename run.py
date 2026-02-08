import os
import sys
import threading
import time
import webbrowser
import uvicorn


def open_browser():
    time.sleep(2)
    webbrowser.open("http://127.0.0.1:8000")


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    BACKEND_DIR = os.path.join(BASE_DIR, "backend")

    os.chdir(BACKEND_DIR)
    sys.path.insert(0, BACKEND_DIR)

    # Otwórz przeglądarkę w tle
    threading.Thread(target=open_browser, daemon=True).start()

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
