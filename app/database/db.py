"""
Modul Database SQLite untuk TaniCek AI (Riwayat Diagnosa & Peta Radar Wabah)
"""

import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent.parent / "tanicek.db"

def get_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS diagnosis_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        crop_name TEXT NOT NULL,
        disease_name TEXT NOT NULL,
        severity TEXT NOT NULL,
        confidence REAL NOT NULL,
        latitude REAL,
        longitude REAL,
        location_name TEXT,
        image_name TEXT,
        emergency_action TEXT,
        organic_solution TEXT,
        chemical_solution TEXT,
        ai_engine TEXT
    )
    """)

    # Cek apakah tabel kosong, jika ya buat beberapa data simulasi awal di lumbung pangan Indonesia
    cursor.execute("SELECT COUNT(*) FROM diagnosis_reports")
    count = cursor.fetchone()[0]

    if count == 0:
        sample_reports = [
            ("2026-09-28 08:30:00", "Padi", "Penyakit Blast (Pyricularia oryzae)", "Kritis", 94.2, -6.3039, 107.3045, "Karawang, Jawa Barat", "sample_blast.jpg", "Keringkan sawah berselang, stop pupuk Urea.", "Ekstrak mimba + Trichoderma", "Trisiklazol 1.5 ml/L", "TaniCek Vision Engine"),
            ("2026-09-28 10:15:00", "Padi", "Hawar Daun Bakteri (Kresek)", "Sedang", 89.5, -6.5500, 107.7600, "Subang, Jawa Barat", "sample_hawar.jpg", "Atur air macak-macak, kurangi Nitrogen.", "Kunyit + lengkuas", "Tembaga Hidroksida", "TaniCek Vision Engine"),
            ("2026-09-28 14:20:00", "Jagung", "Penyakit Bulai Jagung", "Kritis", 96.0, -7.5600, 110.8200, "Klaten, Jawa Tengah", "sample_bulai.jpg", "Cabut tanaman terinfeksi sampai akar lalu kubur.", "Air rebusan sirih", "Perlakuan benih Metalaksil", "TaniCek Vision Engine"),
            ("2026-09-29 07:45:00", "Cabai", "Penyakit Antraknosa (Patek)", "Kritis", 92.8, -7.9800, 112.6300, "Malang, Jawa Timur", "sample_patek.jpg", "Petik seluruh buah terinfeksi dan bakar.", "Ekstrak jahe dan Trichoderma", "Fungisida Mankozeb", "TaniCek Vision Engine"),
            ("2026-09-29 09:10:00", "Padi", "Hama Penggerek Batang (Sundep)", "Sedang", 88.0, -6.3200, 108.3200, "Indramayu, Jawa Barat", "sample_sundep.jpg", "Kumpulkan kelompok telur di daun.", "Lepas parasitoid Trichogramma", "Dimehipo / Karbofuran", "TaniCek Vision Engine"),
            ("2026-09-29 11:30:00", "Padi", "Tanaman Padi Sehat", "Sehat", 98.4, -8.2200, 114.3600, "Banyuwangi, Jawa Timur", "sample_sehat.jpg", "Pertahankan pemupukan berimbang.", "Pupuk Hayati PGPR", "Tidak perlu kimia", "TaniCek Vision Engine"),
            ("2026-09-29 13:00:00", "Jagung", "Hama Ulat Grayak (FAW)", "Kritis", 91.5, -5.3900, 105.2600, "Lampung Tengah, Lampung", "sample_faw.jpg", "Kutip larva di pucuk secara manual.", "Beauveria bassiana", "Klorantraniliprol", "TaniCek Vision Engine")
        ]

        cursor.executemany("""
        INSERT INTO diagnosis_reports (
            timestamp, crop_name, disease_name, severity, confidence,
            latitude, longitude, location_name, image_name, emergency_action,
            organic_solution, chemical_solution, ai_engine
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_reports)

    conn.commit()
    conn.close()

def save_diagnosis(data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
    INSERT INTO diagnosis_reports (
        timestamp, crop_name, disease_name, severity, confidence,
        latitude, longitude, location_name, image_name, emergency_action,
        organic_solution, chemical_solution, ai_engine
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        timestamp,
        data.get("crop_name", "Padi"),
        data.get("disease_name", "Tidak Teridentifikasi"),
        data.get("severity", "Sedang"),
        data.get("confidence", 90.0),
        data.get("latitude", -6.3039),
        data.get("longitude", 107.3045),
        data.get("location_name", "Lahan Pertanian Petani"),
        data.get("image_name", ""),
        data.get("emergency_action", ""),
        data.get("organic_solution", ""),
        data.get("chemical_solution", ""),
        data.get("ai_engine", "TaniCek Vision Engine")
    ))
    report_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return report_id

def get_recent_reports(limit=25):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM diagnosis_reports ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_outbreak_points():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, timestamp, crop_name, disease_name, severity, confidence,
           latitude, longitude, location_name
    FROM diagnosis_reports
    WHERE latitude IS NOT NULL AND longitude IS NOT NULL
    ORDER BY id DESC LIMIT 50
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_statistics():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM diagnosis_reports")
    total_checks = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM diagnosis_reports WHERE severity = 'Kritis'")
    critical_cases = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM diagnosis_reports WHERE severity = 'Sehat'")
    healthy_cases = cursor.fetchone()[0]

    cursor.execute("""
    SELECT crop_name, COUNT(*) as count 
    FROM diagnosis_reports 
    GROUP BY crop_name 
    ORDER BY count DESC
    """)
    crops_dist = [dict(row) for row in cursor.fetchall()]

    conn.close()
    
    # Estimasi ton beras & bahan pangan terselamatkan
    estimated_saved_tons = round(total_checks * 2.8, 1)

    return {
        "total_checks": total_checks,
        "critical_cases": critical_cases,
        "healthy_cases": healthy_cases,
        "estimated_saved_tons": estimated_saved_tons,
        "crops_dist": crops_dist
    }
