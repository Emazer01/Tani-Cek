"""
Generator Dataset Tanaman Pangan Skala Menengah (1,000+ Gambar)
Mencakup 16 kelas penyakit & tanaman sehat untuk Padi, Jagung, Cabai, Bawang, Kedelai, Tomat.
"""

import random
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

DATASET_DIR = Path(__file__).resolve().parent / "data" / "dataset"
TRAIN_DIR = DATASET_DIR / "train"
VAL_DIR = DATASET_DIR / "val"
SAMPLES_DIR = Path(__file__).resolve().parent / "app" / "static" / "images" / "samples"

CLASSES = [
    "padi_blast",
    "padi_hawar_daun",
    "padi_bercak_coklat",
    "padi_sehat",
    "jagung_bulai",
    "jagung_turcicum",
    "jagung_karat",
    "jagung_sehat",
    "cabai_antraknosa",
    "cabai_keriting",
    "cabai_bercak_daun",
    "cabai_sehat",
    "bawang_moler",
    "bawang_trotol",
    "tomat_hawar",
    "kedelai_karat"
]

def make_background(w=224, h=224):
    # Latar tanah atau alam dengan variasi acak
    r = random.randint(210, 245)
    g = random.randint(215, 245)
    b = random.randint(200, 235)
    img = Image.new("RGB", (w, h), color=(r, g, b))
    draw = ImageDraw.Draw(img)
    for _ in range(15):
        x = random.randint(0, w)
        y = random.randint(0, h)
        radius = random.randint(10, 50)
        c = (r + random.randint(-15, 10), g + random.randint(-15, 10), b + random.randint(-15, 10))
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=c)
    return img

def render_plant_class(cls_name, w=224, h=224):
    img = make_background(w, h)
    draw = ImageDraw.Draw(img)

    # 1. PADI BLAST (Belah ketupat runcing, pusat abu-abu tepi coklat)
    if cls_name == "padi_blast":
        # Helaian daun padi
        draw.polygon([(40, 220), (100, 140), (160, 60), (190, 10), (180, 20), (130, 90), (70, 180), (45, 224)], fill=(65, 145, 50))
        draw.line([(42, 222), (185, 15)], fill=(85, 165, 65), width=2)
        # 2-4 bercak belah ketupat
        for _ in range(random.randint(2, 4)):
            cx = random.randint(80, 150)
            cy = random.randint(50, 160)
            rw = random.randint(10, 18)
            rh = random.randint(6, 12)
            draw.polygon([(cx - rw, cy), (cx, cy - rh), (cx + rw, cy), (cx, cy + rh)], fill=(110, 55, 25))
            draw.polygon([(cx - rw//2, cy), (cx, cy - rh//2), (cx + rw//2, cy), (cx, cy + rh//2)], fill=(195, 200, 195))

    # 2. PADI HAWAR DAUN (Tepi mengering kuning keabuan)
    elif cls_name == "padi_hawar_daun":
        draw.polygon([(40, 220), (110, 130), (170, 50), (195, 15), (180, 25), (135, 95), (80, 175), (45, 224)], fill=(68, 140, 48))
        # Hawar di tepi
        draw.polygon([(110, 130), (145, 80), (175, 45), (160, 65), (130, 110), (95, 150)], fill=(215, 185, 60))
        draw.polygon([(125, 105), (155, 60), (170, 48), (150, 75), (130, 105)], fill=(180, 175, 160))

    # 3. PADI BERCAK COKLAT (Bercak lonjong coklat dengan halo kuning)
    elif cls_name == "padi_bercak_coklat":
        draw.polygon([(35, 220), (95, 140), (155, 60), (190, 15), (175, 25), (125, 95), (65, 180), (40, 224)], fill=(70, 150, 55))
        for _ in range(random.randint(4, 7)):
            cx = random.randint(70, 160)
            cy = random.randint(40, 180)
            r = random.randint(4, 9)
            draw.ellipse([cx - r - 2, cy - r - 2, cx + r + 2, cy + r + 2], fill=(220, 200, 70))
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 45, 20))

    # 4. PADI SEHAT (Hijau segar merata)
    elif cls_name == "padi_sehat":
        draw.polygon([(30, 220), (90, 130), (160, 50), (200, 10), (180, 25), (125, 90), (60, 180), (35, 224)], fill=(55, 165, 45))
        draw.line([(32, 222), (195, 15)], fill=(85, 195, 75), width=2)
        # Daun anakan sehat
        draw.polygon([(60, 224), (110, 160), (160, 110), (145, 125), (100, 180), (70, 224)], fill=(65, 175, 55))

    # 5. JAGUNG BULAI (Garis klorosis putih/kuning)
    elif cls_name == "jagung_bulai":
        draw.polygon([(20, 210), (80, 130), (150, 70), (210, 30), (180, 70), (120, 140), (50, 220)], fill=(75, 140, 50))
        for offset in range(-25, 30, 8):
            draw.line([(50 + offset, 190), (110 + offset, 120), (170 + offset, 60)], fill=(240, 235, 165), width=3)

    # 6. JAGUNG TURCICUM (Bercak kumparan lonjong coklat)
    elif cls_name == "jagung_turcicum":
        draw.polygon([(20, 210), (80, 130), (150, 70), (210, 30), (180, 70), (120, 140), (50, 220)], fill=(70, 145, 50))
        for _ in range(random.randint(2, 3)):
            cx = random.randint(70, 140)
            cy = random.randint(70, 150)
            draw.ellipse([cx - 25, cy - 8, cx + 25, cy + 8], fill=(125, 70, 35))
            draw.ellipse([cx - 15, cy - 4, cx + 15, cy + 4], fill=(160, 110, 65))

    # 7. JAGUNG KARAT (Pustul bintil serbuk karat oranye-coklat)
    elif cls_name == "jagung_karat":
        draw.polygon([(20, 210), (80, 130), (150, 70), (210, 30), (180, 70), (120, 140), (50, 220)], fill=(85, 140, 55))
        for _ in range(random.randint(18, 30)):
            px = random.randint(50, 170)
            py = random.randint(50, 180)
            draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(190, 80, 20))
            draw.point((px, py), fill=(225, 120, 30))

    # 8. JAGUNG SEHAT (Daun lebar hijau subur)
    elif cls_name == "jagung_sehat":
        draw.polygon([(15, 215), (75, 125), (145, 65), (215, 25), (185, 65), (125, 135), (45, 220)], fill=(50, 155, 40))
        draw.line([(25, 210), (200, 35)], fill=(75, 180, 65), width=3)

    # 9. CABAI ANTRAKNOSA (Bercak cincin konsentris hitam)
    elif cls_name == "cabai_antraknosa":
        # Buah cabai melengkung
        chili = [(80, 50), (110, 70), (140, 110), (150, 160), (140, 200), (130, 205), (120, 165), (105, 120), (85, 80), (70, 55)]
        draw.polygon(chili, fill=(210, 35, 25))
        # Tangkai
        draw.line([(75, 45), (60, 25)], fill=(55, 120, 45), width=5)
        # Patek cincin
        for _ in range(random.randint(1, 2)):
            cx = random.randint(110, 135)
            cy = random.randint(110, 165)
            draw.ellipse([cx - 16, cy - 14, cx + 16, cy + 14], fill=(75, 25, 20))
            draw.ellipse([cx - 11, cy - 9, cx + 11, cy + 9], fill=(140, 65, 45))
            draw.ellipse([cx - 5, cy - 4, cx + 5, cy + 4], fill=(25, 10, 10))

    # 10. CABAI KERITING (Daun keriting berkerut & kuning klorosis)
    elif cls_name == "cabai_keriting":
        # Daun bergelombang kuning kehijauan
        draw.ellipse([50, 60, 170, 160], fill=(195, 190, 55))
        draw.ellipse([65, 75, 155, 145], fill=(225, 215, 75))
        for i in range(5):
            draw.arc([60 + i*15, 80, 90 + i*15, 130], start=0, end=180, fill=(160, 150, 40), width=2)

    # 11. CABAI BERCAK DAUN (Bercak bulat mata katak)
    elif cls_name == "cabai_bercak_daun":
        draw.ellipse([45, 55, 175, 165], fill=(65, 145, 50))
        draw.line([(110, 55), (110, 165)], fill=(85, 165, 70), width=2)
        for _ in range(random.randint(5, 9)):
            cx = random.randint(65, 155)
            cy = random.randint(70, 150)
            draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(120, 50, 30))
            draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(220, 220, 215))

    # 12. CABAI SEHAT (Daun mulus hijau tua mengkilat)
    elif cls_name == "cabai_sehat":
        draw.ellipse([40, 50, 180, 170], fill=(45, 150, 40))
        draw.line([(110, 50), (110, 170)], fill=(70, 180, 65), width=2)
        draw.ellipse([70, 70, 150, 150], fill=(55, 165, 50))

    # 13. BAWANG MOLER (Daun bawang melintir spiral & kuning layu)
    elif cls_name == "bawang_moler":
        # Daun pipa silinder berputar
        pts = [(60, 210), (80, 170), (120, 140), (140, 90), (110, 60), (130, 20), (145, 25), (125, 65), (155, 95), (135, 145), (95, 175), (75, 215)]
        draw.polygon(pts, fill=(195, 175, 55))
        # Titik pangkal busuk
        draw.ellipse([50, 195, 85, 220], fill=(115, 65, 30))

    # 14. BAWANG TROTOL (Bercak ungu Alternaria)
    elif cls_name == "bawang_trotol":
        draw.polygon([(60, 210), (85, 140), (120, 70), (140, 20), (150, 25), (130, 75), (95, 145), (70, 215)], fill=(75, 150, 60))
        for _ in range(random.randint(2, 4)):
            cx = random.randint(85, 130)
            cy = random.randint(60, 150)
            draw.ellipse([cx - 10, cy - 7, cx + 10, cy + 7], fill=(110, 50, 95)) # Ungu
            draw.ellipse([cx - 5, cy - 3, cx + 5, cy + 3], fill=(155, 95, 140))

    # 15. TOMAT HAWAR (Late blight bercak basah hijau gelap kecoklatan)
    elif cls_name == "tomat_hawar":
        # Daun majemuk tomat
        draw.polygon([(50, 160), (90, 110), (140, 80), (170, 50), (180, 70), (145, 115), (110, 155), (65, 185)], fill=(60, 130, 50))
        # Bercak basah kehitaman
        draw.ellipse([100, 85, 155, 130], fill=(55, 65, 45))
        draw.ellipse([110, 95, 145, 120], fill=(75, 55, 35))
        # Tepi jamur putih
        draw.arc([105, 88, 150, 125], start=45, end=220, fill=(210, 215, 205), width=2)

    # 16. KEDELAI KARAT (Bintil karat rapat pada daun kedelai trifoliate)
    elif cls_name == "kedelai_karat":
        # Daun trifoliate
        draw.ellipse([60, 80, 160, 170], fill=(95, 140, 55))
        for _ in range(random.randint(30, 50)):
            kx = random.randint(70, 150)
            ky = random.randint(90, 160)
            draw.ellipse([kx - 2, ky - 2, kx + 2, ky + 2], fill=(160, 75, 25))

    # Sedikit smoothing & noise realistis
    img = img.filter(ImageFilter.SMOOTH)

    # Random brightness / contrast augmentation
    enh_bright = ImageEnhance.Brightness(img)
    img = enh_bright.enhance(random.uniform(0.9, 1.1))
    enh_contrast = ImageEnhance.Contrast(img)
    img = enh_contrast.enhance(random.uniform(0.92, 1.12))

    return img

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def generate_all_datasets():
    print(f"=== Membuat struktur dataset 16 kelas di {DATASET_DIR} ===")
    TRAIN_DIR.mkdir(parents=True, exist_ok=True)
    VAL_DIR.mkdir(parents=True, exist_ok=True)
    SAMPLES_DIR.mkdir(parents=True, exist_ok=True)

    total_train = 0
    total_val = 0

    for cls in CLASSES:
        cls_train_dir = TRAIN_DIR / cls
        cls_val_dir = VAL_DIR / cls
        cls_train_dir.mkdir(parents=True, exist_ok=True)
        cls_val_dir.mkdir(parents=True, exist_ok=True)

        # 50 training images per class
        for i in range(50):
            img = render_plant_class(cls)
            # Random slight rotation
            img = img.rotate(random.randint(-15, 15), fillcolor=(235, 240, 235))
            img.save(cls_train_dir / f"{cls}_train_{i+1:03d}.jpg", "JPEG", quality=88)
            total_train += 1

        # 15 validation images per class
        for j in range(15):
            img = render_plant_class(cls)
            img = img.rotate(random.randint(-10, 10), fillcolor=(235, 240, 235))
            img.save(cls_val_dir / f"{cls}_val_{j+1:03d}.jpg", "JPEG", quality=88)
            total_val += 1

    print(f"[OK] Selesai: {total_train} sampel training, {total_val} sampel validasi (Total: {total_train + total_val} citra).")

    # Generate sampel baru untuk UI web di app/static/images/samples/
    ui_samples = [
        ("sample_bercak_coklat.jpg", "padi_bercak_coklat"),
        ("sample_jagung_karat.jpg", "jagung_karat"),
        ("sample_cabai_bercak.jpg", "cabai_bercak_daun"),
        ("sample_bawang_moler.jpg", "bawang_moler"),
        ("sample_bawang_trotol.jpg", "bawang_trotol"),
        ("sample_tomat_hawar.jpg", "tomat_hawar"),
        ("sample_kedelai_karat.jpg", "kedelai_karat")
    ]
    for filename, cls in ui_samples:
        s_img = render_plant_class(cls, w=500, h=375)
        s_img.save(SAMPLES_DIR / filename, "JPEG", quality=90)
        print(f"Created UI sample: {filename}")

if __name__ == "__main__":
    generate_all_datasets()
