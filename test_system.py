"""
Unit test internal modul TaniCek AI (tanpa dependensi testclient)
"""
from pathlib import Path
from app.models.ai_vision import AgriVisionAI
from app.models.chat_bot import AgriChatBot
from app.database.db import (
    init_db, save_diagnosis, get_recent_reports, 
    get_outbreak_points, get_statistics
)

import sys
sys.stdout.reconfigure(encoding='utf-8')

def test_database():
    init_db()
    stats = get_statistics()
    assert stats["total_checks"] > 0
    print(f"[OK] Database OK: {stats['total_checks']} diagnosa terdata, ~{stats['estimated_saved_tons']} ton pangan terselamatkan.")

def test_vision_engine():
    ai = AgriVisionAI()
    sample_file = Path("app/static/images/samples/sample_blast.jpg")
    assert sample_file.exists(), "File sampel tidak ditemukan!"
    
    with open(sample_file, "rb") as f:
        img_bytes = f.read()

    res = ai.analyze_image(img_bytes, crop_hint="padi", filename="sample_blast.jpg")
    assert "Blast" in res["disease_name"]
    assert res["severity"] == "Kritis"
    assert len(res["symptoms"]) > 0
    assert len(res["organic_solution"]) > 0
    print(f"[OK] AI Vision Engine OK: {res['crop_name']} -> {res['disease_name']} ({res['confidence']}%)")

def test_chatbot():
    bot = AgriChatBot()
    ans = bot.ask("Bagaimana resep pestisida nabati daun mimba?")
    assert "mimba" in ans.lower()
    print("[OK] AgriBot Penyuluh Pertanian AI OK: Berhasil merespon resep pestisida nabati.")

def test_outbreak_points():
    points = get_outbreak_points()
    assert len(points) > 0
    sample_pt = points[0]
    print(f"[OK] Radar Peta GIS OK: {len(points)} titik wabah terlacak (Contoh: {sample_pt['location_name']} - {sample_pt['disease_name']}).")

if __name__ == "__main__":
    print("\n--- Menjalankan Verifikasi Sistem TaniCek AI ---")
    test_database()
    test_vision_engine()
    test_chatbot()
    test_outbreak_points()
    print("\nSemua modul internal BERHASIL diverifikasi 100%!\n")
