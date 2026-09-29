"""
Modul Tanya Penyuluh AI (AgriBot Konsultasi Pertanian)
"""

import os
import requests
from app.models.disease_db import DISEASE_DATABASE

AGRI_KNOWLEDGE_FAQ = {
    "pupuk": (
        "💡 **Panduan Pemupukan Berimbang Tanaman Pangan:**\n\n"
        "1. **Padi Sawah:** Gunakan prinsip 5T (Tepat Jenis, Dosis, Waktu, Tempat, dan Cara).\n"
        "   - **Dasar (0-7 HST):** Urea 75 kg + SP-36 100 kg + KCl 50 kg / ha.\n"
        "   - **Susulan I (21-25 HST):** Urea 100 kg + Phonska 150 kg / ha.\n"
        "   - **Susulan II (35-40 HST):** Urea 50 kg + KCl 50 kg / ha untuk pengisian bulir.\n"
        "2. **Peringatan Penting:** Hindari memberikan pupuk Nitrogen (Urea) berlebihan saat cuaca mendung/hujan lebat, karena dinding sel tanaman akan rapuh dan sangat rentan diserang jamur Blast dan hawar bakteri."
    ),
    "pestisida nabati": (
        "🌿 **Resep & Cara Pembuatan Pestisida Nabati Daun Mimba & Bawang Putih:**\n\n"
        "**Bahan:**\n"
        "- 1 kg daun mimba segar (bisa diganti daun tembakau / mahoni)\n"
        "- 100 gram bawang putih\n"
        "- 1 sendok makan sabun cuci piring (sebagai pelekat/perata alami)\n"
        "- 10 liter air bersih\n\n"
        "**Cara Membuat:**\n"
        "1. Tumbuk halus daun mimba dan bawang putih.\n"
        "2. Rendam dalam 10 liter air selama 24 jam.\n"
        "3. Saring larutan menggunakan kain kasa halus.\n"
        "4. Tambahkan sabun cuci piring lalu aduk rata.\n"
        "5. **Aplikasi:** Semprotkan ke daun tanaman pada pagi hari (sebelum pukul 09.00) atau sore hari (setelah pukul 15.30)."
    ),
    "waktu semprot": (
        "⏰ **Waktu Terbaik Penyemprotan Pestisida & Fungisida:**\n\n"
        "- **Pagi Hari (06.30 - 09.00 WIB):** Saat stomata daun masih terbuka dan angin belum kencang, sehingga penyerapan obat sistemik maksimal.\n"
        "- **Sore Hari (15.30 - 17.30 WIB):** Sangat efektif untuk hama nokturnal (ulat grayak, wereng) dan aplikasi agens hayati (Trichoderma, Beauveria) agar spora tidak mati terkena sinar UV matahari terik.\n"
        "- **PENTING:** Jangan pernah menyemprot saat terik siang hari (11.00 - 14.00) karena cairan cepat menguap dan daun bisa terbakar (fitotoksik), atau saat mendung tebal menjelang hujan lebat."
    ),
    "wereng": (
        "🦗 **Pengendalian Terpadu Hama Wereng Coklat (Nilaparvata lugens):**\n\n"
        "1. **Keringkan Sawah (Intermittent):** Wereng menyukai kanopi yang lembap dan becek. Mengeringkan sawah selama 3-5 hari efektif memutus siklus bertelur.\n"
        "2. **Bahan Aktif Kimia:** Gunakan insektisida berbahan aktif Pimetrozin (contoh: Chess), Buprofezin (Applaud), atau Tiametoksam. Arahkan nozzle semprot tepat ke **pangkal batang padi**, bukan ke pucuk daun!\n"
        "3. **Musuh Alami:** Jaga laba-laba serigala (*Pardosa pseudoannulata*) dan kepik mirid dengan tidak menyemprot insektisida piretroid spektrum luas di awal tanam."
    ),
    "tikus": (
        "🐀 **Pengendalian Hama Tikus Sawah (TBS & Sanitasi):**\n\n"
        "1. Terapkan **TBS (Trap Barrier System)** dengan tanaman perangkap yang ditanam 2-3 minggu lebih awal.\n"
        "2. Gropyokan massal bersama seluruh anggota kelompok tani di awal musim sebelum masa tanam.\n"
        "3. Pasang rumah burung hantu (Rubuha) untuk burung hantu Tyto alba (1 pasang burung hantu mampu memangsa 2-5 ekor tikus per malam).\n"
        "4. Bersihkan tanggul pematang sawah agar tidak menjadi sarang."
    )
}

class AgriChatBot:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")

    def ask(self, user_question: str, custom_api_key: str = None) -> str:
        """Menjawab pertanyaan seputar agronomi dan perlindungan tanaman."""
        active_key = custom_api_key or self.api_key
        
        # 1. Coba Gemini jika ada API key
        if active_key and len(active_key.strip()) > 10:
            try:
                ans = self._ask_gemini(user_question, active_key)
                if ans:
                    return ans
            except Exception as e:
                print(f"[Warning] Chatbot Gemini error: {e}")

        # 2. Heuristic Agronomy FAQ Matcher
        q_lower = user_question.lower()
        for keyword, response in AGRI_KNOWLEDGE_FAQ.items():
            if keyword in q_lower:
                return response

        # Default jawaban komprehensif
        return (
            "🌾 **Halo Petani Hebat!** Saya AgriBot, Asisten Penyuluh Pertanian AI TaniCek.\n\n"
            f"Pertanyaan Anda: *\"{user_question}\"*\n\n"
            "Untuk ketahanan pangan optimal, berikut rekomendasi dasar:\n"
            "- Pastikan diagnosa hama/penyakit tepat sebelum membeli obat dengan fitur **Deteksi Foto** TaniCek.\n"
            "- Prioritaskan pengendalian ramah lingkungan (agen hayati Trichoderma/Beauveria atau pestisida nabati).\n"
            "- Lakukan rotasi tanaman dan sanitasi gulma di pematang sawah.\n\n"
            "*(💡 Tip: Anda dapat menanyakan tentang cara pemupukan, resep pestisida nabati, pengendalian wereng, atau waktu semprot terbaik).* "
            "Untuk analisis mendalam real-time, Anda juga bisa memasukkan Gemini API Key di menu Pengaturan."
        )

    def _ask_gemini(self, question: str, api_key: str) -> str:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
        prompt = f"""
Anda adalah Petugas Penyuluh Pertanian Lapangan (PPL) dan Ahli Agronomi Indonesia yang ramah, solutif, dan berwawasan luas.
Bantu petani menjawab pertanyaan berikut secara praktis, terukur, dan mengutamakan ketahanan pangan serta keamanan lingkungan.
Pertanyaan Petani: {question}

Gunakan gaya bahasa Indonesia yang santun, jelas, terstruktur rapi dengan poin-poin/bullet, dan cantumkan dosis serta takaran bahan jika relevan.
"""
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.4}
        }
        resp = requests.post(url, headers={"Content-Type": "application/json"}, json=payload, timeout=20)
        if resp.status_code == 200:
            candidates = resp.json().get("candidates", [])
            if candidates:
                return candidates[0]["content"]["parts"][0]["text"]
        return None
