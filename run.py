"""
Script untuk menjalankan server TaniCek AI
"""
import sys
import uvicorn
from app.config import HOST, PORT

if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(f"=== Memulai server TaniCek AI pada http://{HOST}:{PORT} ===")
    print("Tekan Ctrl+C untuk menghentikan server.")
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=False)
