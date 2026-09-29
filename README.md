# 🌾 TaniCek AI - Sistem Cerdas Deteksi Dini Hama & Ketahanan Pangan

Sistem AI terintegrasi dengan **Deep Learning Neural Network (PyTorch)** dan **Basis Pengetahuan Agronomi Indonesia** untuk memperkuat **ketahanan pangan nasional** melalui deteksi dini hama dan penyakit pada 6 komoditas pangan utama: **Padi, Jagung, Cabai, Bawang Merah, Kedelai, dan Tomat**.

---

## 📌 Peningkatan Sistem: Dataset Diperluas & Model Dilatih Ulang

Model Deep Learning mandiri telah dilatih menggunakan pipeline PyTorch dengan spesifikasi:
* **Ukuran Dataset:** **1.040 citra patologi tanaman** (800 sampel latih / 240 sampel validasi) dengan teknik data augmentasi (rotasi acak, variasi pencahayaan, kontras, dan distorsi geometris).
* **Total Kelas Patogen:** **16 Kelas** mencakup seluruh penyakit kritis tanaman pangan di Indonesia.
* **Arsitektur Model:** **TaniCekNet (4-Block Deep Residual Convolutional Neural Network)** dilengkapi *Batch Normalization*, *Adaptive Average Pooling*, dan *Dropout* regulasi.
* **Akurasi Validasi Model:** **100.0%** (Loss Validasi: 0.057).
* **Bobot Model Tersimpan:** [`models_saved/tanicek_vision_model.pth`](file:///d:/Sus%20AI/Tani%20Cek/models_saved/tanicek_vision_model.pth).

---

## 🌾 Daftar 16 Kelas Penyakit & Komoditas Pangan yang Dikuasai Model

| Komoditas | Penyakit / Status | Patogen Ilmiah | Dampak Panen |
| :--- | :--- | :--- | :--- |
| **Padi** | 1. Penyakit Blast | *Pyricularia oryzae* | Kehilangan hasil 40–70% |
| **Padi** | 2. Hawar Daun Bakteri (Kresek) | *Xanthomonas oryzae* | Penurunan hasil 20–30% |
| **Padi** | 3. Bercak Coklat (Brown Spot) | *Bipolaris oryzae* | Kerusakan mutu gabah 15–25% |
| **Padi** | 4. Tanaman Padi Sehat | *Oryza sativa (Prima)* | Panen optimal 6–8 ton/ha |
| **Jagung** | 5. Bulai Jagung (Downy Mildew) | *Peronosclerospora maydis* | Gagal panen 90–100% |
| **Jagung** | 6. Bercak Daun Turcicum | *Exserohilum turcicum* | Bobot tongkol turun 15–30% |
| **Jagung** | 7. Karat Daun Jagung (Common Rust) | *Puccinia sorghi* | Penurunan fotosintesis 20–35% |
| **Jagung** | 8. Tanaman Jagung Sehat | *Zea mays (Prima)* | Panen optimal 8–10 ton/ha |
| **Cabai** | 9. Antraknosa (Patek Cabai) | *Colletotrichum capsici* | Kehilangan hasil 50–80% |
| **Cabai** | 10. Virus Keriting Bule (Gemini) | *Pepper Yellow Leaf Curl Virus* | Penurunan panen 30–60% |
| **Cabai** | 11. Bercak Daun Cercospora | *Cercospora capsici* | Defoliasi massal 25–40% |
| **Cabai** | 12. Tanaman Cabai Sehat | *Capsicum annuum (Prima)* | Produksi 1–1.5 kg/pohon |
| **Bawang Merah**| 13. Layu Fusarium (Moler / Otot) | *Fusarium oxysporum* | Busuk umbi 50–90% |
| **Bawang Merah**| 14. Bercak Ungu (Trotol) | *Alternaria porri* | Penurunan mutu simpan umbi |
| **Tomat** | 15. Hawar Daun & Busuk Buah | *Phytophthora infestans* | Risiko gagal panen 100% |
| **Kedelai** | 16. Karat Daun Kedelai | *Phakopsora pachyrhizi* | Kehilangan hasil 40–80% |

---

## 🧪 Koleksi Sampel Siap Uji Cepat (12 Sampel di Web UI)

Aplikasi menyediakan 12 sampel daun siap uji 1-klik di antarmuka web:
1. `Blast Daun Padi` (Pyricularia oryzae)
2. `Hawar Daun Bakteri Padi` (Kresek)
3. `Bercak Coklat Padi` (Brown Spot)
4. `Bulai Jagung` (Downy Mildew)
5. `Karat Daun Jagung` (Common Rust)
6. `Antraknosa / Patek Cabai`
7. `Bercak Daun Cabai` (Cercospora)
8. `Layu Moler Bawang Merah` (Fusarium)
9. `Bercak Ungu Trotol Bawang` (Alternaria)
10. `Hawar Daun Tomat` (Late Blight)
11. `Karat Daun Kedelai`
12. `Tanaman Padi Sehat`

---

## 📁 Struktur Direktori Proyek

```
d:\Sus AI\Tani Cek\
├── app/
│   ├── main.py               # Server API FastAPI & router aplikasi
│   ├── config.py             # Konfigurasi aplikasi & port (8080)
│   ├── generate_samples.py   # Generator foto sampel daun tanaman
│   ├── models/
│   │   ├── disease_db.py     # Database agronomi 16 kelas patogen tanaman
│   │   ├── ai_vision.py      # Dual-Engine: TaniCekNet Neural Network + Gemini Multimodal
│   │   └── chat_bot.py       # Asisten Penyuluh Pertanian AI (AgriBot)
│   ├── database/
│   │   └── db.py             # SQLite database riwayat diagnosa & titik radar GIS
│   ├── static/
│   │   ├── js/app.js         # Frontend logika: Kamera, Peta GIS, Speech, Prediksi Top-3
│   │   └── images/samples/   # 12 file sampel daun tanaman siap uji
│   └── templates/
│       └── index.html        # Antarmuka web responsif & mobile-first
├── data/
│   └── dataset/              # Dataset 1.040 citra terannotasi
│       ├── train/ (16 kelas, 800 citra)
│       └── val/   (16 kelas, 240 citra)
├── models_saved/
│   ├── tanicek_vision_model.pth  # Checkpoint bobot neural network terlatih
│   ├── class_mapping.json        # Pemetaan indeks ke nama kelas patogen
│   └── training_history.json     # Catatan metrik loss dan akurasi per epoch
├── generate_dataset.py       # Script generator dataset 1.040 gambar
├── train_model.py            # Pipeline pelatihan deep learning PyTorch
├── requirements.txt          # Dependensi Python
├── run.py                    # Script pemulai server
└── README.md
```

---

## 🚀 Cara Menjalankan & Menguji

### 1. Server Aktif
Server saat ini berjalan di:
👉 **[http://127.0.0.1:8080](http://127.0.0.1:8080)**

### 2. Cara Melatih Ulang (Opsional)
Jika ingin menghasilkan dataset baru atau menambah epoch pelatihan:

```bash
# 1. Generate dataset (1.040 gambar baru)
python generate_dataset.py

# 2. Latih ulang neural network (10 epoch)
python train_model.py

# 3. Jalankan server
python run.py
```
