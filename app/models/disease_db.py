"""
Database Pengetahuan Hama & Penyakit Tanaman Pangan Indonesia (TaniCek Knowledge Base)
Disesuaikan dengan panduan Kementerian Pertanian RI, BPTP, dan Pengendalian Hama Terpadu (PHT).
Versi Dataset Diperluas: Padi, Jagung, Cabai, Bawang Merah, Kedelai, Tomat.
"""

CROPS = {
    "padi": "Padi (Oryza sativa) - Tanaman Pangan Utama",
    "jagung": "Jagung (Zea mays) - Pangan & Pakan Ternak",
    "cabai": "Cabai Merah / Rawit (Capsicum spp.) - Komoditas Strategis",
    "bawang": "Bawang Merah (Allium cepa) - Bumbu & Pangan Pokok",
    "kedelai": "Kedelai (Glycine max) - Sumber Protein Nabati",
    "tomat": "Tomat (Solanum lycopersicum) - Hortikultura Pangan"
}

DISEASE_DATABASE = {
    # ------------------ PADI ------------------
    "padi_blast": {
        "crop": "padi",
        "crop_name": "Padi",
        "disease_name": "Penyakit Blast (Pyricularia oryzae)",
        "scientific_name": "Magnaporthe oryzae (Pyricularia oryzae)",
        "category": "Jamur / Fungi",
        "severity": "Kritis",
        "confidence_range": (88, 97),
        "symptoms": [
            "Bercak belah ketupat runcing di kedua ujung pada helaian daun",
            "Pusat bercak berwarna abu-abu keputihan dengan tepi coklat kemerahan",
            "Pada fase generatif menyerang leher malai (blast leher/patah leher), menyebabkan bulir gabah hampa",
            "Menular sangat cepat saat kelembapan udara >90% dan embun pagi tinggi"
        ],
        "emergency_action": "Segera keringkan sawah (drainase berselang), kurangi genangan air, dan stop aplikasi pupuk Nitrogen/Urea seketika karena memperlemah dinding sel tanaman.",
        "organic_solution": "Semprotkan ekstrak daun mimba (Azadirachta indica) dicampur rendaman bawang putih (200 gr/10 liter air) atau aplikasikan agens hayati Trichoderma viride / Pseudomonas fluorescens pada sore hari.",
        "chemical_solution": "Fungisida berbahan aktif Trisiklazol (contoh: Beam 75 WP), Azoksistrobin + Difenokonazol (contoh: Amistar Top), atau Kasugamisin. Dosis: 1.0 - 1.5 ml/liter air.",
        "prevention": "Gunakan varietas tahan (Inpari 32, Inpari 42, Inpago 9), terapkan perlakuan benih (seed treatment), dan jaga jarak tanam legowo 2:1 atau 4:1.",
        "food_security_impact": "Dapat menurunkan produksi beras hingga 40-70% jika mengenai fase pembentukan malai. Penyelamatan dini mengamankan rata-rata 3-4 ton gabah kering panen per hektar."
    },
    "padi_hawar_daun": {
        "crop": "padi",
        "crop_name": "Padi",
        "disease_name": "Hawar Daun Bakteri / Kresek (Xanthomonas oryzae)",
        "scientific_name": "Xanthomonas oryzae pv. oryzae",
        "category": "Bakteri",
        "severity": "Sedang",
        "confidence_range": (85, 95),
        "symptoms": [
            "Bercak basah bergaris di tepi daun yang meluas memanjang ke pangkal",
            "Warna daun berubah dari kuning pucat menjadi putih keabu-abuan mirip daun terbakar",
            "Pada pagi hari keluar tetesan lendir bakteri berwarna kuning keemasan di tepi daun",
            "Daun cepat menggulung dan mengering"
        ],
        "emergency_action": "Hindari pemotongan ujung bibit saat pindah tanam, atur air macak-macak (jangan digenangi terus menerus), dan seimbangkan pupuk dengan Kalium (KCl).",
        "organic_solution": "Semprotkan perasan rimpang kunyit dan lengkuas (mengandung kurkuminoid antibakteri alami) serta agens antagonis Paenibacillus polymyxa.",
        "chemical_solution": "Bakterisida berbahan aktif Tembaga Oksiklorida (contoh: Kuproxat), Tembaga Hidroksida (Kocide), atau Asam Oksolinik (Starner). Dosis: 1.5-2 gr/liter air.",
        "prevention": "Gunakan benih bersertifikat bebas bakteri, bersihkan gulma inang di pematang sawah, dan rotasi tanaman.",
        "food_security_impact": "Menyebabkan bulir padi berkerut dan pengisian malai tidak optimal, berpotensi menurunkan hasil 20-30%."
    },
    "padi_bercak_coklat": {
        "crop": "padi",
        "crop_name": "Padi",
        "disease_name": "Bercak Coklat Padi (Brown Spot)",
        "scientific_name": "Bipolaris oryzae (Helminthosporium oryzae)",
        "category": "Jamur / Fungi",
        "severity": "Sedang",
        "confidence_range": (86, 95),
        "symptoms": [
            "Bercak lonjong atau bulat berwarna coklat gelap dengan halo kuning di sekelilingnya",
            "Bercak tersebar merata di seluruh helaian daun dan bulir padi",
            "Sering menjadi indikator tanah kekurangan unsur hara mikro (K, Fe, Zn, Mn) atau kekeringan"
        ],
        "emergency_action": "Lakukan pemupukan susulan berimbang Kalium (KCl) dan aplikasi pupuk mikro daun yang mengandung Silika (Si) dan Zinc (Zn).",
        "organic_solution": "Aplikasi mikroba tanah Streptomyces sp. dan Trichoderma, serta penambahan kompos jerami yang telah terdekomposisi matang.",
        "chemical_solution": "Fungisida Mankozeb (Dithane M-45) atau Propikonazol (Tilt 250 EC) dosis 1.5-2 ml/liter.",
        "prevention": "Perbaiki kesuburan tanah dengan pemupukan organik dan drainase yang baik.",
        "food_security_impact": "Dapat menurunkan bobot 1000 butir gabah dan menurunkan mutu beras giling hingga 15-25%."
    },
    "padi_tungro": {
        "crop": "padi",
        "crop_name": "Padi",
        "disease_name": "Penyakit Tungro (Virus Tungro Padi)",
        "scientific_name": "Rice Tungro Bacilliform Virus (RTBV) ditularkan Wereng Hijau (Nephotettix virescens)",
        "category": "Virus & Vektor Hama",
        "severity": "Kritis",
        "confidence_range": (86, 96),
        "symptoms": [
            "Daun menguning oranye mulai dari pucuk daun yang lebih tua",
            "Pertumbuhan tanaman kerdil nyata dan jumlah anakan sangat sedikit",
            "Malai yang keluar pendek, kecil, dan tidak keluar sempurna",
            "Kehadiran wereng daun hijau di pangkal rumpun padi"
        ],
        "emergency_action": "Cabut dan musnahkan (eradikasi) rumpun yang terserang parah agar tidak menjadi sumber inokulum bagi rumpun lain di sekitarnya.",
        "organic_solution": "Kendalikan wereng hijau dengan jamur entomopatogen Beauveria bassiana dan semprot ekstrak tembakau/biji mimba.",
        "chemical_solution": "Kendalikan vektor wereng hijau dengan insektisida sistemik berbahan aktif Dinotefuran, Imidakloprid, atau Pimetrozin.",
        "prevention": "Tanam serempak dalam satu hamparan (rentang waktu maksimal 2 minggu), gunakan varietas tahan wereng hijau (Inpari 36 Lanrang).",
        "food_security_impact": "Epidemi mematikan bagi padi. Tanaman terinfeksi awal tidak menghasilkan gabah sama sekali (100% loss per rumpun)."
    },
    "padi_sehat": {
        "crop": "padi",
        "crop_name": "Padi",
        "disease_name": "Tanaman Padi Sehat",
        "scientific_name": "Oryza sativa (Kondisi Prima)",
        "category": "Sehat",
        "severity": "Sehat",
        "confidence_range": (94, 99),
        "symptoms": [
            "Helaian daun berwarna hijau segar merata tanpa bercak nekrotik",
            "Anakan produktif tumbuh kokoh dan tegak",
            "Batang bersih dari lubang hama dan perakaran putih kecokelatan sehat"
        ],
        "emergency_action": "Pertahankan pola pemupukan berimbang (Urea + SP-36 + KCl + Pupuk Organik) dan sirkulasi air yang teratur.",
        "organic_solution": "Aplikasi PGPR (Plant Growth-Promoting Rhizobacteria) atau Pupuk Organik Cair (POC) secara berkala.",
        "chemical_solution": "Tidak memerlukan pestisida kimia. Tetap lakukan monitoring rutin mingguan.",
        "prevention": "Jaga kebersihan pematang sawah dan pertahankan populasi musuh alami.",
        "food_security_impact": "Potensi hasil maksimal 6-8 ton gabah kering giling per hektar tercapai dengan optimal."
    },

    # ------------------ JAGUNG ------------------
    "jagung_bulai": {
        "crop": "jagung",
        "crop_name": "Jagung",
        "disease_name": "Penyakit Bulai Jagung (Downy Mildew)",
        "scientific_name": "Peronosclerospora maydis",
        "category": "Jamur / Oomycota",
        "severity": "Kritis",
        "confidence_range": (89, 98),
        "symptoms": [
            "Garis klorosis memanjang warna putih atau kuning sejajar tulang daun",
            "Pada pagi hari di bawah permukaan daun terdapat lapisan spora seperti bedak tepung putih",
            "Tanaman kerdil, daun kaku dan tegak lurus, tongkol tidak terisi sempurna atau tidak keluar sama sekali"
        ],
        "emergency_action": "Cabut tanaman terinfeksi sampai akarnya (eradikasi), masukkan ke kantong plastik, bakar/kubur di luar lahan.",
        "organic_solution": "Semprotkan air rebusan sirih dan kunyit, serta inokulasi benih dengan jamur Trichoderma harzianum sebelum tanam.",
        "chemical_solution": "Perlakuan benih (seed treatment) wajib menggunakan Metalaksil (contoh: Saromyl / Ridomil Gold) dosis 2 gr/kg benih.",
        "prevention": "Pilih varietas hibrida tahan bulai (Pioneer P35, NK Perkasa, Bisi 18) dan tanam serempak di awal musim hujan.",
        "food_security_impact": "Penyebab nomor 1 gagal panen jagung di Indonesia dengan potensi kehilangan hasil hingga 90-100% pada umur muda."
    },
    "jagung_turcicum": {
        "crop": "jagung",
        "crop_name": "Jagung",
        "disease_name": "Bercak Daun Turcicum / Hawar Daun Jagung",
        "scientific_name": "Exserohilum turcicum (Bipolaris turcica)",
        "category": "Jamur / Fungi",
        "severity": "Sedang",
        "confidence_range": (84, 94),
        "symptoms": [
            "Bercak memanjang seperti bentuk perahu atau kumparan (panjang 3-15 cm)",
            "Awalnya bercak berwarna hijau kelabu lalu berubah menjadi coklat kering",
            "Bercak meluas dan menyatu hingga daun mengering sebelum waktunya"
        ],
        "emergency_action": "Pangkas daun bawah yang terserang parah untuk mengurangi kelembapan kanopi mikro.",
        "organic_solution": "Semprot biopestisida jamur antagonis Gliocladium sp. atau ekstrak lengkuas.",
        "chemical_solution": "Fungisida berbahan aktif Mankozeb (Dithane M-45), Klorotalonil, atau Azoksistrobin. Dosis 2 gr/liter.",
        "prevention": "Gunakan jarak tanam yang longgar (70 x 20 cm) dan bersihkan sisa brangkasan jagung yang sakit.",
        "food_security_impact": "Mengurangi fotosintesis saat pengisian biji, memangkas bobot tongkol 15-30%."
    },
    "jagung_karat": {
        "crop": "jagung",
        "crop_name": "Jagung",
        "disease_name": "Penyakit Karat Daun Jagung (Common Rust)",
        "scientific_name": "Puccinia sorghi",
        "category": "Jamur / Fungi",
        "severity": "Sedang",
        "confidence_range": (85, 95),
        "symptoms": [
            "Bintil-bintil kecil (pustul) timbul berwarna coklat kemerahan mirip serbuk karat besi",
            "Pustul tersebar pada kedua permukaan daun atas dan bawah",
            "Jika diusap dengan jari, serbuk spora berwarna coklat menempel di tangan",
            "Daun yang terserang parah akan menguning dan robek-robek"
        ],
        "emergency_action": "Pangkas daun terinfeksi di lapisan bawah kanopi dan hindari penyiraman dari atas daun saat sore hari.",
        "organic_solution": "Semprot larutan belerang (sulfur) organik atau ekstrak rimpang kunyit.",
        "chemical_solution": "Fungisida berbahan aktif Tebukonazol (Folicur), Mankozeb, atau Azoksistrobin. Dosis 1.5-2 gr/liter.",
        "prevention": "Gunakan varietas tahan karat dan hindari penanaman di dataran tinggi yang lembap dan dingin di luar musim.",
        "food_security_impact": "Dapat mengurangi bobot tongkol hingga 20-35% jika menyerang sebelum fase penyerbukan."
    },
    "jagung_sehat": {
        "crop": "jagung",
        "crop_name": "Jagung",
        "disease_name": "Tanaman Jagung Sehat",
        "scientific_name": "Zea mays (Kondisi Prima)",
        "category": "Sehat",
        "severity": "Sehat",
        "confidence_range": (95, 99),
        "symptoms": [
            "Daun hijau tua lebar dan mulus bebas dari garis klorosis maupun robekan ulat",
            "Batang kokoh, perakaran serabut kuat, rambut tongkol segar"
        ],
        "emergency_action": "Lanjutkan pemupukan fase generatif (NPK Phonska) dan pengairan teratur saat pembungaan.",
        "organic_solution": "Tambahkan pupuk kandang matang atau pupuk hayati mikoriza untuk penyerapan hara optimal.",
        "chemical_solution": "Tidak diperlukan pestisida kimia.",
        "prevention": "Pantau kebun 2 kali seminggu untuk deteksi dini serangan serangga.",
        "food_security_impact": "Potensi hasil panen maksimal 8-10 ton pipil kering per hektar."
    },

    # ------------------ CABAI ------------------
    "cabai_antraknosa": {
        "crop": "cabai",
        "crop_name": "Cabai",
        "disease_name": "Penyakit Antraknosa / Patek Cabai",
        "scientific_name": "Colletotrichum capsici / Colletotrichum acutatum",
        "category": "Jamur / Fungi",
        "severity": "Kritis",
        "confidence_range": (90, 98),
        "symptoms": [
            "Bercak melingkar cekung (lesio) berwarna coklat kehitaman pada buah cabai",
            "Bercak membentuk cincin konsentris dengan titik hitam di tengahnya",
            "Buah cabai busuk kering, mengkerut, dan rontok sebelum matang",
            "Serangan meningkat tajam saat musim hujan dan drainase buruk"
        ],
        "emergency_action": "Petik seluruh buah cabai yang terinfeksi patek sesegera mungkin, masukkan kantong, lalu kubur jauh dari kebun. Jangan dibuang di parit!",
        "organic_solution": "Semprotkan air rebusan daun sirih merah + ekstrak jahe dan lengkuas. Taburkan Trichoderma di sekitar perakaran.",
        "chemical_solution": "Fungisida berbahan aktif Mankozeb, Tembaga Oksiklorida, Propineb (Antracol), atau Difenokonazol. Dosis 2 gr/liter.",
        "prevention": "Gunakan mulsa plastik hitam perak, perlebar jarak tanam (minimal 60 cm), dan hindari pupuk N berlebih saat hujan.",
        "food_security_impact": "Penyebab utama lonjakan harga cabai nasional. Kehilangan hasil cabai dapat mencapai 50-80% dalam 1 pekan hujan terus menerus."
    },
    "cabai_keriting": {
        "crop": "cabai",
        "crop_name": "Cabai",
        "disease_name": "Penyakit Virus Kuning / Keriting Bule (Gemini Virus)",
        "scientific_name": "Pepper Yellow Leaf Curl Virus (ditularkan Kutu Kebul Bemisia tabaci)",
        "category": "Virus & Vektor Hama",
        "severity": "Sedang",
        "confidence_range": (87, 96),
        "symptoms": [
            "Helaian daun muda mengeriting kaku ke atas dan mengkerut",
            "Warna daun berubah menjadi kuning cerah mencolok dengan tulang daun tetap hijau",
            "Tanaman kerdil, ruas batang memendek, pembentukan bunga rontok"
        ],
        "emergency_action": "Beri pupuk daun mikro (Zn, Fe, Mg) untuk menstimulasi daun baru dan cabut tanaman yang kerdil sejak dini.",
        "organic_solution": "Semprotkan pestisida nabati minyak mimba (neem oil) atau ekstrak cabai rawit + sabun cuci piring (surfaktan alami).",
        "chemical_solution": "Kendalikan vektor kutu kebul dengan insektisida berbahan aktif Imidakloprid (Confidor), Abamektin, atau Tiametoksam.",
        "prevention": "Pasang perangkap lem kuning (yellow sticky trap) 40 buah/hektar dan gunakan bibit toleran seperti varietas Laba F1 atau Imola.",
        "food_security_impact": "Mengurangi hasil panen buah cabai 30-60% serta memperpendek usia produktif tanaman cabai."
    },
    "cabai_bercak_daun": {
        "crop": "cabai",
        "crop_name": "Cabai",
        "disease_name": "Bercak Daun Cercospora (Katak-katakan)",
        "scientific_name": "Cercospora capsici",
        "category": "Jamur / Fungi",
        "severity": "Sedang",
        "confidence_range": (85, 94),
        "symptoms": [
            "Bercak bulat kecil warna abu-abu keputihan dengan tepi coklat tua kemerahan",
            "Bercak mirip mata katak pada permukaan helaian daun",
            "Daun yang terserang parah cepat menguning dan gugur secara massal (defoliasi)",
            "Buah terpapar sinar matahari langsung dan mengalami sengatan (sunscald)"
        ],
        "emergency_action": "Kumpulkan dan musnahkan daun-daun gugur di bawah tanaman untuk memutus siklus inokulum jamur.",
        "organic_solution": "Aplikasi biofungisida jamur Trichoderma harzianum dan semprot rebusan daun sirih.",
        "chemical_solution": "Fungisida berbahan aktif Klorotalonil (Daconil), Propineb, atau Tembaga Hidroksida. Dosis 2 gr/liter.",
        "prevention": "Gunakan mulsa dan atur jarak tanam agar pertukaran udara lancar di bawah rimbun cabai.",
        "food_security_impact": "Gugurnya daun menurunkan kapasitas fotosintesis dan mengurangi jumlah buah panen hingga 25-40%."
    },
    "cabai_sehat": {
        "crop": "cabai",
        "crop_name": "Cabai",
        "disease_name": "Tanaman Cabai Sehat",
        "scientific_name": "Capsicum annuum (Kondisi Prima)",
        "category": "Sehat",
        "severity": "Sehat",
        "confidence_range": (94, 99),
        "symptoms": [
            "Daun hijau mengkilap rata tanpa kerutan",
            "Bunga mekar sempurna dan bakal buah lebat mulus mengkilat",
            "Pertumbuhan cabang kokoh dan seimbang"
        ],
        "emergency_action": "Jaga kecukupan air dengan irigasi tetes atau siram teratur, berikan kalsium (Ca) agar buah tidak pecah.",
        "organic_solution": "Semprot pupuk organik cair asam amino dan perbanyak mikoriza di akar.",
        "chemical_solution": "Tidak memerlukan pestisida kimia.",
        "prevention": "Pertahankan gulma bersih dan sanitasi lahan berkala.",
        "food_security_impact": "Produksi cabai optimal 1-1.5 kg per pohon."
    },

    # ------------------ BAWANG MERAH ------------------
    "bawang_moler": {
        "crop": "bawang",
        "crop_name": "Bawang Merah",
        "disease_name": "Penyakit Layu Fusarium / Moler / Otot",
        "scientific_name": "Fusarium oxysporum f.sp. cepae",
        "category": "Jamur / Fungi",
        "severity": "Kritis",
        "confidence_range": (88, 97),
        "symptoms": [
            "Daun bawang melintir atau terpuntir berputar menyerupai spiral (gejala moler)",
            "Pangkal batang semu dan umbi membusuk basah dan berbau",
            "Akar membusuk dan mudah tercabut dari tanah",
            "Daun menguning mulai dari ujung lalu layu secara menyeluruh"
        ],
        "emergency_action": "Cabut segera tanaman yang moler, buang jauh dari bedengan, dan taburkan kapur dolomit di bekas lubang tanam untuk menetralkan pH tanah.",
        "organic_solution": "Campurkan Trichoderma sp. dan Gliocladium ke dalam pupuk kandang matang saat olah tanah (200 kg/ha).",
        "chemical_solution": "Kocorkan fungisida berbahan aktif Benomil atau Mankozeb + Karbendazim pada pangkal rumpun yang mulai tergejala.",
        "prevention": "Rotasi tanaman dengan padi (pola Padi - Bawang - Palawija), gunakan benih bebas Fusarium, dan pastikan bedengan tinggi dengan drainase lancar.",
        "food_security_impact": "Penyakit paling mematikan bagi petani bawang merah di sentra Brebes & Nganjuk, dapat memangkas panen hingga 50-90% saat musim hujan."
    },
    "bawang_trotol": {
        "crop": "bawang",
        "crop_name": "Bawang Merah",
        "disease_name": "Bercak Ungu / Trotol Bawang Merah",
        "scientific_name": "Alternaria porri",
        "category": "Jamur / Fungi",
        "severity": "Sedang",
        "confidence_range": (86, 95),
        "symptoms": [
            "Bercak kecil melekuk berwarna keputihan yang kemudian meluas menjadi bercak keunguan dengan tepi coklat",
            "Pada permukaan bercak tampak cincin-cincin konsentris warna gelap",
            "Ujung daun patah atau rebah layu pada titik bercak",
            "Umbi bawang mengecil dan busuk kering saat disimpan di gudang"
        ],
        "emergency_action": "Kurangi frekuensi penyiraman di sore hari dan semprot fungisida protektif pada saat kabut/embun pagi hilang.",
        "organic_solution": "Semprot ekstrak daun cengkeh dan bakteri antagonis Bacillus subtilis.",
        "chemical_solution": "Fungisida berbahan aktif Difenokonazol (Score 250 EC) atau Propineb (Antracol 70 WP). Dosis: 1.5-2 gr/liter.",
        "prevention": "Jemur benih bawang merah hingga kering sempurna sebelum ditanam dan bersihkan gulma di parit.",
        "food_security_impact": "Menurunkan mutu ukuran umbi bawang merah dan mempercepat kebusukan umbi di penyimpanan gudang."
    },

    # ------------------ KEDELAI ------------------
    "kedelai_karat": {
        "crop": "kedelai",
        "crop_name": "Kedelai",
        "disease_name": "Penyakit Karat Daun Kedelai",
        "scientific_name": "Phakopsora pachyrhizi",
        "category": "Jamur / Fungi",
        "severity": "Kritis",
        "confidence_range": (87, 96),
        "symptoms": [
            "Bintil-bintil kecil warna coklat kemerahan pada permukaan bawah helaian daun kedelai",
            "Daun menguning lebih awal dan rontok sebelum fase pengisian polong tuntas",
            "Polong yang terbentuk hampa atau biji berukuran sangat kecil berkerut"
        ],
        "emergency_action": "Segera lakukan penyemprotan fungisida sistemik begitu ditemukan 1-2 bintil karat per tanaman pada fase berbunga.",
        "organic_solution": "Semprot biopestisida jamur Beauveria bassiana atau ekstrak daun mimba.",
        "chemical_solution": "Fungisida berbahan aktif Triazol (Tebukonazol, Difenokonazol, atau Heksakonazol) dosis 1-1.5 ml/liter.",
        "prevention": "Tanam varietas tahan karat (seperti varietas Anjasmoro, Dega 1, atau Argomulyo) dan tanam serempak.",
        "food_security_impact": "Kedelai merupakan bahan baku utama tempe & tahu nasional. Karat daun dapat menurunkan produksi kedelai hingga 40-80%."
    },

    # ------------------ TOMAT ------------------
    "tomat_hawar": {
        "crop": "tomat",
        "crop_name": "Tomat",
        "disease_name": "Hawar Daun & Busuk Buah Tomat (Late Blight)",
        "scientific_name": "Phytophthora infestans",
        "category": "Oomycota / Jamur",
        "severity": "Kritis",
        "confidence_range": (90, 98),
        "symptoms": [
            "Bercak basah berwarna hijau kelabu gelap tidak beraturan pada daun dan batang",
            "Pada cuaca lembap, di bawah bercak terdapat lapisan jamur halus berwarna putih kelabu",
            "Buah tomat muncul bercak coklat kehitaman keras bergelombang lalu membusuk",
            "Penyebaran sangat masif dalam 2-3 hari saat suhu sejuk dan kabut tebal"
        ],
        "emergency_action": "Pangkas dan bakar seluruh bagian tanaman yang busuk, hindari penyiraman membasahi daun, dan semprot fungisida tembaga.",
        "organic_solution": "Semprot larutan bubur bordeaux (campuran kapur tohor dan terusi tembaga sulfat) atau Trichoderma harzianum.",
        "chemical_solution": "Fungisida berbahan aktif Dimetomorf (Acrobat), Simoksanil, atau Mankozeb. Dosis 2 gr/liter.",
        "prevention": "Pasang naungan plastik hujan (rain shelter) dan gunakan jarak tanam lebar (60 x 50 cm).",
        "food_security_impact": "Dapat memusnahkan seluruh tanaman tomat dalam satu hamparan (gagal panen 100%) dalam kurun waktu 1 minggu."
    }
}
