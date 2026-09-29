"""
Script pembuat sampel gambar daun tanaman untuk pengujian instan TaniCek AI.
"""
from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent.parent / "app" / "static" / "images" / "samples"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def create_sample_blast():
    # Daun padi hijau panjang dengan bercak belah ketupat Blast
    img = Image.new("RGB", (600, 450), color=(240, 248, 240))
    draw = ImageDraw.Draw(img)

    # Latar belakang tanah / sawah blur
    draw.rectangle([0, 0, 600, 450], fill=(225, 235, 220))

    # Helaian daun padi
    leaf_coords = [(80, 420), (220, 250), (320, 160), (450, 60), (520, 20), (510, 40), (420, 120), (300, 220), (160, 360), (100, 450)]
    draw.polygon(leaf_coords, fill=(78, 148, 56))

    # Tulang daun
    draw.line([(90, 435), (515, 30)], fill=(96, 172, 70), width=3)

    # Bercak blast 1 (belah ketupat)
    lesion1 = [(260, 200), (280, 185), (310, 200), (290, 215)]
    draw.polygon(lesion1, fill=(110, 60, 30))
    # Pusat abu-abu
    inner1 = [(270, 200), (280, 192), (300, 200), (290, 208)]
    draw.polygon(inner1, fill=(190, 195, 190))

    # Bercak blast 2
    lesion2 = [(350, 130), (370, 115), (400, 130), (380, 145)]
    draw.polygon(lesion2, fill=(110, 60, 30))
    inner2 = [(360, 130), (370, 122), (390, 130), (380, 138)]
    draw.polygon(inner2, fill=(200, 205, 200))

    # Bercak blast kecil 3
    draw.ellipse([210, 260, 235, 275], fill=(120, 70, 35))
    draw.ellipse([216, 264, 229, 271], fill=(185, 190, 185))

    img = img.filter(ImageFilter.SMOOTH_MORE)
    img.save(OUT_DIR / "sample_blast.jpg", "JPEG", quality=90)
    print("Created sample_blast.jpg")

def create_sample_hawar():
    # Hawar daun bakteri (tepi daun mengering kekuningan keabuan)
    img = Image.new("RGB", (600, 450), color=(235, 240, 235))
    draw = ImageDraw.Draw(img)

    # Daun
    draw.polygon([(100, 430), (250, 260), (380, 140), (530, 30), (480, 90), (340, 210), (180, 360), (120, 440)], fill=(75, 145, 50))
    # Tulang daun
    draw.line([(110, 435), (505, 60)], fill=(95, 170, 70), width=3)

    # Hawar bakteri di tepi daun (gelombang kuning ke abu-abu)
    blight = [(350, 170), (420, 100), (490, 50), (460, 110), (380, 190), (320, 240)]
    draw.polygon(blight, fill=(215, 180, 70))
    blight_inner = [(380, 140), (440, 80), (480, 60), (450, 100), (400, 150)]
    draw.polygon(blight_inner, fill=(180, 175, 160))

    img = img.filter(ImageFilter.SMOOTH)
    img.save(OUT_DIR / "sample_hawar.jpg", "JPEG", quality=90)
    print("Created sample_hawar.jpg")

def create_sample_bulai():
    # Daun jagung lebar dengan garis klorosis putih/kuning
    img = Image.new("RGB", (600, 450), color=(238, 242, 235))
    draw = ImageDraw.Draw(img)

    # Helaian daun jagung
    draw.polygon([(50, 400), (150, 280), (300, 180), (500, 80), (550, 60), (480, 140), (320, 260), (160, 380), (70, 430)], fill=(80, 140, 55))

    # Garis-garis bulai (kuning keputihan memanjang sejajar)
    for offset in range(-30, 40, 12):
        draw.line([(100 + offset, 380), (250 + offset, 240), (420 + offset, 130)], fill=(235, 230, 160), width=5)

    img = img.filter(ImageFilter.SMOOTH)
    img.save(OUT_DIR / "sample_bulai.jpg", "JPEG", quality=90)
    print("Created sample_bulai.jpg")

def create_sample_patek():
    # Buah cabai merah dengan bercak patek cekung melingkar
    img = Image.new("RGB", (600, 450), color=(245, 245, 240))
    draw = ImageDraw.Draw(img)

    # Tangkai cabai
    draw.line([(180, 90), (230, 140)], fill=(65, 120, 45), width=8)

    # Buah cabai melengkung
    chili_pts = [(220, 135), (280, 170), (340, 220), (380, 290), (400, 370), (380, 375), (340, 310), (280, 240), (230, 180), (200, 140)]
    draw.polygon(chili_pts, fill=(210, 40, 30))

    # Bercak antraknosa konsentris
    draw.ellipse([270, 210, 315, 255], fill=(70, 20, 15))
    draw.ellipse([280, 220, 305, 245], fill=(130, 60, 40))
    draw.ellipse([288, 228, 297, 237], fill=(30, 10, 10))

    # Bercak kecil kedua
    draw.ellipse([325, 265, 350, 290], fill=(80, 25, 20))
    draw.ellipse([332, 272, 343, 283], fill=(140, 70, 50))

    img = img.filter(ImageFilter.SMOOTH)
    img.save(OUT_DIR / "sample_patek.jpg", "JPEG", quality=90)
    print("Created sample_patek.jpg")

def create_sample_sehat():
    # Daun padi hijau segar sehat tanpa cacat
    img = Image.new("RGB", (600, 450), color=(235, 245, 235))
    draw = ImageDraw.Draw(img)

    # Daun utama
    draw.polygon([(60, 420), (200, 270), (340, 170), (480, 80), (540, 30), (510, 70), (400, 170), (260, 280), (120, 410)], fill=(60, 160, 50))
    # Tulang daun
    draw.line([(70, 430), (530, 40)], fill=(85, 190, 70), width=4)

    # Daun kedua (anakan)
    draw.polygon([(150, 440), (260, 310), (390, 210), (470, 160), (440, 190), (330, 290), (210, 390)], fill=(75, 175, 60))

    img = img.filter(ImageFilter.SMOOTH_MORE)
    img.save(OUT_DIR / "sample_sehat.jpg", "JPEG", quality=90)
    print("Created sample_sehat.jpg")

if __name__ == "__main__":
    create_sample_blast()
    create_sample_hawar()
    create_sample_bulai()
    create_sample_patek()
    create_sample_sehat()
    print("All sample images generated successfully!")
