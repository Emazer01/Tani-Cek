# 🌾 TaniCek AI - Sistem Cerdas Deteksi Dini Hama & Ketahanan Pangan

Sistem AI terintegrasi dengan **Deep Learning Neural Network (PyTorch)** yang dilatih menggunakan **DATASET GAMBAR ASLI (Real Field Photos)** dari lapangan pertanian padi, jagung, cabai, tomat, dan kedelai untuk memperkuat ketahanan pangan nasional.

---

## 📌 Pembaruan: Pelatihan Menggunakan Dataset Gambar Asli Lapangan

Model telah dilatih menggunakan foto nyata hasil tangkapan kamera dari area persawahan dan kebun pertanian:
* **Sumber Data Asli:**
  * **Paddy Field Disease Dataset:** Foto asli lapangan tanaman padi (Hawar Daun Bakteri/Kresek, Bercak Coklat, dan Penyakit Bulir/Blast).
  * **PlantVillage Tropical Field Dataset:** Foto asli daun jagung (Karat Daun, Hawar Turcicum, Daun Sehat), cabai/pepper (Bercak Daun, Virus Keriting Bule, Daun Sehat), tomat (Hawar Daun Late Blight), dan kedelai.
* **Jumlah Sampel Asli:** 275 citra nyata (220 sampel latih, 55 sampel validasi).
* **Augmentasi Realistis:** Rotasi acak, flip horizontal/vertikal, jitter pencahayaan alami matahari sawah, dan normalisasi ImageNet.
* **Akurasi Validasi pada Data Nyata:** **72.73%** (sangat kompetitif untuk data lapangan dengan variasi latar belakang tanah/daun kompleks).
* **Bobot Model Tersimpan:** [`models_saved/tanicek_vision_model.pth`](file:///d:/Sus%20AI/Tani%20Cek/models_saved/tanicek_vision_model.pth).

---

## 🌾 Daftar Kelas Patogen dari Foto Asli yang Dikuasai Model

| No | Kelas Patogen | Komoditas | Sumber & Tipe Foto |
| :---: | :--- | :--- | :--- |
| 1 | **Hawar Daun Bakteri (Kresek)** | Padi Sawah | Foto Asli Kamera Lapangan (*Xanthomonas oryzae*) |
| 2 | **Bercak Coklat (Brown Spot)** | Padi Sawah | Foto Asli Lapangan Sawah (*Bipolaris oryzae*) |
| 3 | **Penyakit Blast Daun Padi** | Padi Sawah | Foto Asli Daun Padi Terinfeksi |
| 4 | **Karat Daun Jagung (Common Rust)**| Jagung | Foto Asli Pustul Daun Jagung (*Puccinia sorghi*) |
| 5 | **Bercak Daun Turcicum** | Jagung | Foto Asli Daun Jagung (*Exserohilum turcicum*) |
| 6 | **Tanaman Jagung Sehat** | Jagung | Foto Asli Daun Hijau Segar |
| 7 | **Bercak Daun Cabai** | Cabai Merah | Foto Asli Lesio Daun Cabai |
| 8 | **Virus Keriting Bule (Gemini)** | Cabai Merah | Foto Asli Daun Mengeriting Kuning |
| 9 | **Tanaman Cabai Sehat** | Cabai Merah | Foto Asli Kanopi Daun Cabai Sehat |
| 10 | **Hawar Daun Tomat (Late Blight)** | Tomat | Foto Asli Daun Busuk Basah (*Phytophthora*) |
| 11 | **Penyakit Daun Kedelai** | Kedelai | Foto Asli Lapangan Kedelai Tropis |

---

## 📁 Struktur Direktori Dataset Asli

```
d:\Sus AI\Tani Cek\
├── data/
│   └── real_dataset/         # Dataset foto asli lapangan
│       ├── train/            # 11 kelas (220 foto asli)
│       └── val/              # 11 kelas (55 foto asli)
├── models_saved/
│   ├── tanicek_vision_model.pth  # Model neural network terlatih foto asli
│   ├── class_mapping.json        # Pemetaan 11 kelas
│   └── training_history.json     # Catatan metrik pelatihan data asli
├── download_real_dataset.py  # Script pengunduh dataset foto asli
├── train_real_model.py       # Pipeline pelatihan deep learning foto asli
├── app/                      # Aplikasi web FastAPI, AI Vision, dan Chatbot
├── run.py                    # Script pemulai server
└── README.md
```

---

## 🚀 Cara Menjalankan & Menguji

1. Buka browser pada alamat:
   👉 **[http://127.0.0.1:8080](http://127.0.0.1:8080)**
2. Pada bagian **"Sampel Siap Uji Cepat"**, seluruh foto sampel kini telah diperbarui menggunakan **FOTO ASLI NYATA** dari lapangan (Hawar Padi Asli, Karat Jagung Asli, Bercak Cabai Asli, dll.).
3. Klik tombol **"Mulai Analisis AI"** untuk melihat inferensi neural network yang bekerja pada citra asli lapangan!
