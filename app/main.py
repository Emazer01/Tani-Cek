"""
TaniCek AI - Aplikasi Utama (FastAPI)
Sistem Pintar Deteksi Dini Hama & Penyakit Tanaman Pangan untuk Ketahanan Pangan
"""

import os
import json
import shutil
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from app.config import STATIC_DIR, TEMPLATES_DIR, UPLOAD_DIR, SAMPLE_DIR, HOST, PORT
from app.models.ai_vision import AgriVisionAI
from app.models.chat_bot import AgriChatBot
from app.database.db import (
    init_db, save_diagnosis, get_recent_reports, 
    get_outbreak_points, get_statistics
)

# Inisialisasi database
init_db()

app = FastAPI(
    title="TaniCek AI",
    description="Sistem Deteksi Hama & Penyakit Tanaman Pangan Berbasis AI",
    version="1.0.0"
)

# Mounting folder statis
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

# Inisialisasi AI engines
vision_ai = AgriVisionAI()
chat_bot = AgriChatBot()

class ChatRequest(BaseModel):
    message: str
    api_key: str = ""

@app.get("/", response_class=HTMLResponse)
async def index_page(request: Request):
    """Halaman utama TaniCek AI"""
    return templates.TemplateResponse(request=request, name="index.html")

@app.post("/api/diagnose")
async def diagnose_crop(
    image: UploadFile = File(None),
    sample_name: str = Form(None),
    crop_hint: str = Form(""),
    notes: str = Form(""),
    latitude: float = Form(None),
    longitude: float = Form(None),
    location_name: str = Form(""),
    api_key: str = Form("")
):
    """
    Endpoint diagnosa foto tanaman pangan.
    Menerima file upload atau pilihan sampel yang sudah tersedia.
    """
    image_bytes = None
    filename = ""

    if image and image.filename:
        filename = image.filename
        image_bytes = await image.read()
        # Simpan file upload ke disk
        save_path = UPLOAD_DIR / filename
        with open(save_path, "wb") as f:
            f.write(image_bytes)
    elif sample_name:
        filename = sample_name
        sample_path = SAMPLE_DIR / sample_name
        if not sample_path.exists():
            raise HTTPException(status_code=404, detail="File sampel tidak ditemukan")
        with open(sample_path, "rb") as f:
            image_bytes = f.read()
    else:
        raise HTTPException(status_code=400, detail="Harap unggah gambar atau pilih salah satu sampel daun.")

    # Analisis dengan AI Vision
    diagnosis = vision_ai.analyze_image(
        image_bytes=image_bytes,
        crop_hint=crop_hint,
        filename=filename,
        custom_api_key=api_key
    )

    # Simpan ke database riwayat & peta radar wabah
    record_data = {
        "crop_name": diagnosis.get("crop_name", crop_hint or "Padi"),
        "disease_name": diagnosis.get("disease_name", "Penyakit Tanaman"),
        "severity": diagnosis.get("severity", "Sedang"),
        "confidence": diagnosis.get("confidence", 90.0),
        "latitude": latitude or -6.3039,
        "longitude": longitude or 107.3045,
        "location_name": location_name or "Lahan Pertanian Petani",
        "image_name": filename,
        "emergency_action": diagnosis.get("emergency_action", ""),
        "organic_solution": diagnosis.get("organic_solution", ""),
        "chemical_solution": diagnosis.get("chemical_solution", ""),
        "ai_engine": diagnosis.get("ai_engine", "TaniCek Engine")
    }
    report_id = save_diagnosis(record_data)
    diagnosis["report_id"] = report_id

    return JSONResponse(content={"status": "success", "data": diagnosis})

@app.post("/api/chat")
async def chat_with_agribot(req: ChatRequest):
    """Endpoint konsultasi tanya jawab dengan Penyuluh AI"""
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Pesan tidak boleh kosong")
    
    reply = chat_bot.ask(req.message, custom_api_key=req.api_key)
    return JSONResponse(content={"status": "success", "reply": reply})

@app.get("/api/reports")
async def list_reports(limit: int = 20):
    """Mengambil daftar riwayat diagnosa terkini"""
    reports = get_recent_reports(limit=limit)
    return JSONResponse(content={"status": "success", "reports": reports})

@app.get("/api/outbreak-map")
async def outbreak_map_data():
    """Mengambil data koordinat sebaran serangan hama untuk radar peta"""
    points = get_outbreak_points()
    return JSONResponse(content={"status": "success", "points": points})

@app.get("/api/statistics")
async def dashboard_statistics():
    """Statistik dampak ketahanan pangan nasional TaniCek"""
    stats = get_statistics()
    return JSONResponse(content={"status": "success", "stats": stats})

@app.get("/api/samples")
async def available_samples():
    """Daftar sampel gambar daun tanaman siap uji (diperluas 12 sampel)"""
    samples = [
        {
            "id": "sample_blast.jpg",
            "name": "Blast Daun Padi (Pyricularia)",
            "crop": "Padi",
            "category": "Jamur Kritis",
            "url": "/static/images/samples/sample_blast.jpg",
            "description": "Bercak belah ketupat runcing tengah abu-abu"
        },
        {
            "id": "sample_hawar.jpg",
            "name": "Hawar Daun Bakteri (Kresek)",
            "crop": "Padi",
            "category": "Bakteri",
            "url": "/static/images/samples/sample_hawar.jpg",
            "description": "Pinggiran daun mengering bergelombang"
        },
        {
            "id": "sample_bercak_coklat.jpg",
            "name": "Bercak Coklat Padi (Brown Spot)",
            "crop": "Padi",
            "category": "Jamur Fungi",
            "url": "/static/images/samples/sample_bercak_coklat.jpg",
            "description": "Bercak lonjong dengan halo kuning"
        },
        {
            "id": "sample_bulai.jpg",
            "name": "Bulai Jagung (Downy Mildew)",
            "crop": "Jagung",
            "category": "Jamur Kritis",
            "url": "/static/images/samples/sample_bulai.jpg",
            "description": "Garis putih kuning memanjang sejajar tulang daun"
        },
        {
            "id": "sample_jagung_karat.jpg",
            "name": "Karat Daun Jagung (Common Rust)",
            "crop": "Jagung",
            "category": "Jamur Karat",
            "url": "/static/images/samples/sample_jagung_karat.jpg",
            "description": "Pustul bintil serbuk karat oranye coklat"
        },
        {
            "id": "sample_patek.jpg",
            "name": "Antraknosa / Patek Cabai",
            "crop": "Cabai",
            "category": "Jamur Buah",
            "url": "/static/images/samples/sample_patek.jpg",
            "description": "Bercak melingkar cekung konsentris pada buah"
        },
        {
            "id": "sample_cabai_bercak.jpg",
            "name": "Bercak Daun Cabai (Cercospora)",
            "crop": "Cabai",
            "category": "Jamur Daun",
            "url": "/static/images/samples/sample_cabai_bercak.jpg",
            "description": "Bercak bulat mata katak abu-abu tepi merah"
        },
        {
            "id": "sample_bawang_moler.jpg",
            "name": "Layu Fusarium / Moler Bawang",
            "crop": "Bawang Merah",
            "category": "Jamur Kritis",
            "url": "/static/images/samples/sample_bawang_moler.jpg",
            "description": "Daun melintir spiral dan umbi membusuk"
        },
        {
            "id": "sample_bawang_trotol.jpg",
            "name": "Bercak Ungu / Trotol Bawang",
            "crop": "Bawang Merah",
            "category": "Jamur Fungi",
            "url": "/static/images/samples/sample_bawang_trotol.jpg",
            "description": "Bercak cekung keunguan Alternaria"
        },
        {
            "id": "sample_tomat_hawar.jpg",
            "name": "Hawar Daun Tomat (Late Blight)",
            "crop": "Tomat",
            "category": "Jamur Kritis",
            "url": "/static/images/samples/sample_tomat_hawar.jpg",
            "description": "Bercak basah hijau gelap cepat meluas"
        },
        {
            "id": "sample_kedelai_karat.jpg",
            "name": "Karat Daun Kedelai",
            "crop": "Kedelai",
            "category": "Jamur Pangan",
            "url": "/static/images/samples/sample_kedelai_karat.jpg",
            "description": "Bintil karat rapat pada daun trifoliate"
        },
        {
            "id": "sample_sehat.jpg",
            "name": "Tanaman Padi Sehat",
            "crop": "Padi",
            "category": "Kondisi Prima",
            "url": "/static/images/samples/sample_sehat.jpg",
            "description": "Daun hijau segar mulus bebas bercak nekrotik"
        }
    ]
    return JSONResponse(content={"status": "success", "samples": samples})

@app.get("/api/model-info")
async def model_info():
    """Mengambil informasi arsitektur dan riwayat pelatihan model PyTorch"""
    report_file = Path(__file__).resolve().parent.parent / "models_saved" / "training_history.json"
    if report_file.exists():
        with open(report_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return JSONResponse(content={"status": "success", "model_info": data})
    return JSONResponse(content={
        "status": "success",
        "model_info": {
            "model_name": "MobileNetV3-Small (PyTorch Deep Learning)",
            "num_classes": 16,
            "status": "Siap"
        }
    })
