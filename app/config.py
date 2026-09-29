"""
TaniCek AI - Konfigurasi Aplikasi
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Muat file .env jika ada
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "app" / "static"
TEMPLATES_DIR = BASE_DIR / "app" / "templates"
SAMPLE_DIR = STATIC_DIR / "images" / "samples"
UPLOAD_DIR = BASE_DIR / "uploads"

# Buat direktori jika belum ada
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
SAMPLE_DIR.mkdir(parents=True, exist_ok=True)

# Kunci API Gemini (Opsional: bisa diisi di .env atau via UI oleh pengguna)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# Pengaturan Server
HOST = os.getenv("HOST", "127.0.0.1")
PORT = int(os.getenv("PORT", 8080))
