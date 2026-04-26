from flask import Flask, render_template, request, jsonify
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

app = Flask(__name__)


def build_fis():
    # ── Antecedents ──────────────────────────────────────────────
    kelelahan     = ctrl.Antecedent(np.arange(0, 11, 0.1), 'kelelahan')
    durasi        = ctrl.Antecedent(np.arange(0, 13, 0.1), 'durasi')
    mood_awal     = ctrl.Antecedent(np.arange(0, 11, 0.1), 'mood_awal')
    tidur         = ctrl.Antecedent(np.arange(0, 11, 0.1), 'tidur')
    introvert_lvl = ctrl.Antecedent(np.arange(0, 11, 0.1), 'introvert_lvl')

    # ── Consequent ───────────────────────────────────────────────
    recovery = ctrl.Consequent(np.arange(0, 25, 0.1), 'recovery')

    # ── MF: kelelahan ────────────────────────────────────────────
    kelelahan['rendah']  = fuzz.trapmf(kelelahan.universe, [0, 0, 2, 4])
    kelelahan['sedang']  = fuzz.trimf (kelelahan.universe, [3, 5, 7])
    kelelahan['tinggi']  = fuzz.trapmf(kelelahan.universe, [6, 8, 10, 10])

    # ── MF: durasi (jam) ─────────────────────────────────────────
    durasi['singkat']  = fuzz.trapmf(durasi.universe, [0, 0, 1, 2])
    durasi['sedang']   = fuzz.trimf (durasi.universe, [1, 3, 6])
    durasi['panjang']  = fuzz.trapmf(durasi.universe, [5, 7, 12, 12])

    # ── MF: mood_awal ────────────────────────────────────────────
    mood_awal['buruk']  = fuzz.trapmf(mood_awal.universe, [0, 0, 2, 4])
    mood_awal['netral'] = fuzz.trimf (mood_awal.universe, [3, 5, 7])
    mood_awal['baik']   = fuzz.trapmf(mood_awal.universe, [6, 8, 10, 10])

    # ── MF: tidur (jam) ──────────────────────────────────────────
    tidur['kurang'] = fuzz.trapmf(tidur.universe, [0, 0, 4, 6])
    tidur['cukup']  = fuzz.trimf (tidur.universe, [5, 7, 8.5])
    tidur['lebih']  = fuzz.trapmf(tidur.universe, [8, 9, 10, 10])

    # ── MF: introvert_level ──────────────────────────────────────
    introvert_lvl['ekstrovert'] = fuzz.trapmf(introvert_lvl.universe, [0, 0, 2, 4])
    introvert_lvl['ambivert']   = fuzz.trimf (introvert_lvl.universe, [3, 5, 7])
    introvert_lvl['introvert']  = fuzz.trapmf(introvert_lvl.universe, [6, 8, 10, 10])

    # ── MF: recovery (jam) ───────────────────────────────────────
    recovery['sangat_singkat'] = fuzz.trapmf(recovery.universe, [0, 0, 1, 3])
    recovery['singkat']        = fuzz.trimf (recovery.universe, [2, 4, 6])
    recovery['sedang']         = fuzz.trimf (recovery.universe, [5, 8, 11])
    recovery['panjang']        = fuzz.trimf (recovery.universe, [9, 13, 17])
    recovery['sangat_panjang'] = fuzz.trapmf(recovery.universe, [15, 19, 24, 24])

    # ── Rule Base (25 rules) ─────────────────────────────────────
    rules = [
        # Kelelahan rendah
        ctrl.Rule(kelelahan['rendah'] & durasi['singkat'] & mood_awal['baik'],
                  recovery['sangat_singkat']),
        ctrl.Rule(kelelahan['rendah'] & durasi['singkat'] & introvert_lvl['ekstrovert'],
                  recovery['sangat_singkat']),
        ctrl.Rule(kelelahan['rendah'] & durasi['sedang'] & mood_awal['baik'] & tidur['cukup'],
                  recovery['singkat']),
        ctrl.Rule(kelelahan['rendah'] & durasi['sedang'] & introvert_lvl['ambivert'],
                  recovery['singkat']),
        ctrl.Rule(kelelahan['rendah'] & durasi['panjang'] & introvert_lvl['introvert'],
                  recovery['sedang']),
        ctrl.Rule(kelelahan['rendah'] & mood_awal['buruk'],
                  recovery['sedang']),
        ctrl.Rule(kelelahan['rendah'] & tidur['kurang'],
                  recovery['singkat']),

        # Kelelahan sedang
        ctrl.Rule(kelelahan['sedang'] & durasi['singkat'] & mood_awal['baik'],
                  recovery['singkat']),
        ctrl.Rule(kelelahan['sedang'] & durasi['singkat'] & introvert_lvl['ekstrovert'],
                  recovery['singkat']),
        ctrl.Rule(kelelahan['sedang'] & durasi['sedang'] & tidur['cukup'],
                  recovery['sedang']),
        ctrl.Rule(kelelahan['sedang'] & durasi['sedang'] & tidur['kurang'],
                  recovery['panjang']),
        ctrl.Rule(kelelahan['sedang'] & durasi['panjang'] & introvert_lvl['introvert'],
                  recovery['panjang']),
        ctrl.Rule(kelelahan['sedang'] & durasi['panjang'] & mood_awal['buruk'],
                  recovery['sangat_panjang']),
        ctrl.Rule(kelelahan['sedang'] & mood_awal['buruk'] & tidur['kurang'],
                  recovery['panjang']),
        ctrl.Rule(kelelahan['sedang'] & introvert_lvl['ambivert'],
                  recovery['sedang']),

        # Kelelahan tinggi
        ctrl.Rule(kelelahan['tinggi'] & durasi['singkat'] & tidur['lebih'],
                  recovery['sedang']),
        ctrl.Rule(kelelahan['tinggi'] & durasi['singkat'] & introvert_lvl['introvert'],
                  recovery['panjang']),
        ctrl.Rule(kelelahan['tinggi'] & durasi['sedang'],
                  recovery['panjang']),
        ctrl.Rule(kelelahan['tinggi'] & durasi['panjang'],
                  recovery['sangat_panjang']),
        ctrl.Rule(kelelahan['tinggi'] & tidur['kurang'],
                  recovery['sangat_panjang']),
        ctrl.Rule(kelelahan['tinggi'] & mood_awal['buruk'],
                  recovery['sangat_panjang']),
        ctrl.Rule(kelelahan['tinggi'] & introvert_lvl['introvert'] & tidur['kurang'],
                  recovery['sangat_panjang']),

        # Tidur & mood dominan
        ctrl.Rule(tidur['kurang'] & mood_awal['buruk'] & introvert_lvl['introvert'],
                  recovery['sangat_panjang']),
        ctrl.Rule(tidur['lebih'] & mood_awal['baik'] & introvert_lvl['ekstrovert'],
                  recovery['sangat_singkat']),
        ctrl.Rule(mood_awal['baik'] & tidur['cukup'] & introvert_lvl['ambivert'],
                  recovery['singkat']),
    ]

    system = ctrl.ControlSystem(rules)
    return ctrl.ControlSystemSimulation(system)


# ── Lazy initialization — build FIS hanya saat pertama kali dipakai ──
_fis = None

def get_fis():
    global _fis
    if _fis is None:
        _fis = build_fis()
    return _fis


def run_fis(kelelahan_val, durasi_val, mood_val, tidur_val, introvert_val):
    fis = get_fis()  # lazy load

    kelelahan_val  = float(np.clip(kelelahan_val,  0, 10))
    durasi_val     = float(np.clip(durasi_val,     0, 12))
    mood_val       = float(np.clip(mood_val,       0, 10))
    tidur_val      = float(np.clip(tidur_val,      0, 10))
    introvert_val  = float(np.clip(introvert_val,  0, 10))

    fis.input['kelelahan']     = kelelahan_val
    fis.input['durasi']        = durasi_val
    fis.input['mood_awal']     = mood_val
    fis.input['tidur']         = tidur_val
    fis.input['introvert_lvl'] = introvert_val
    fis.compute()

    recovery_hours = round(float(fis.output['recovery']), 1)
    energy_raw = 100 - (kelelahan_val * 8) - (durasi_val * 1.2) + (tidur_val * 1.5) + (mood_val * 0.8)
    energy_pct = int(np.clip(energy_raw, 5, 95))
    return recovery_hours, energy_pct


# ════════════════════════════════════════════════════════════════
#  EXPERT SYSTEM — Identifikasi Jenis Kulit & Skincare
#  Metode : Forward-chaining rule-based
#  Input  : jenis kulit, masalah utama, reaksi terhadap produk
#  Output : diagnosis + rutinitas pagi/malam + bahan aktif
# ════════════════════════════════════════════════════════════════

KNOWLEDGE_BASE = [
    {
        "id": "oily_acne",
        "cond": lambda m, c, r: m == "oily" and (c == "acne" or r == "breakout"),
        "type": "Berminyak & berjerawat",
        "desc": "Produksi sebum berlebih menyumbat pori dan memicu breakout. Fokus pada kontrol minyak, anti-inflamasi, dan pencegahan penyumbatan pori.",
        "morning": ["Gentle foaming cleanser (salicylic acid 0.5–2%)", "Niacinamide serum 10%", "Oil-free non-comedogenic moisturizer", "SPF 30–50 ringan"],
        "evening": ["Double cleanse (oil + gentle foam)", "BHA toner", "Retinol atau adapalene (2–3x/minggu)", "Light gel moisturizer"],
        "ingredients": ["Salicylic Acid", "Niacinamide", "Benzoyl Peroxide", "Adapalene", "Zinc PCA"],
        "avoid": ["Heavy cream berlemak", "Coconut oil", "Alkohol konsentrasi tinggi", "Comedogenic oils"],
    },
    {
        "id": "oily_aging",
        "cond": lambda m, c, r: m == "oily" and c == "aging",
        "type": "Berminyak & anti-aging",
        "desc": "Kulit berminyak dengan tanda penuaan dini. Butuh kontrol sebum sekaligus antioksidan dan booster kolagen.",
        "morning": ["Foaming cleanser", "Vitamin C serum (L-ascorbic acid)", "Lightweight moisturizer", "SPF 30–50"],
        "evening": ["Double cleanse", "Retinol (mulai rendah, naikkan bertahap)", "Gel moisturizer"],
        "ingredients": ["Vitamin C", "Retinol", "Peptide", "Niacinamide", "AHA"],
        "avoid": ["Heavy emollient", "Skip SPF", "Mineral oil"],
    },
    {
        "id": "oily_stable",
        "cond": lambda m, c, r: m == "oily",
        "type": "Berminyak normal",
        "desc": "Sebum tinggi tanpa masalah signifikan. Prioritas regulasi minyak dan menjaga pori tetap bersih.",
        "morning": ["Gel cleanser ringan", "Hyaluronic acid serum", "Oil-free moisturizer", "SPF 30+"],
        "evening": ["Double cleanse", "AHA/BHA toner (2–3x/minggu)", "Light moisturizer"],
        "ingredients": ["Niacinamide", "Hyaluronic Acid", "AHA", "BHA", "Green Tea"],
        "avoid": ["Heavy oil", "Produk oklusif berat", "Comedogenic moisturizer"],
    },
    {
        "id": "dry_sensitive",
        "cond": lambda m, c, r: m == "dry" and (c == "sensitive" or r == "irritate"),
        "type": "Kering & sensitif",
        "desc": "Skin barrier lemah membuat kulit reaktif sekaligus kehilangan kelembapan. Pendekatan minimal dengan bahan calming dan barrier repair.",
        "morning": ["Creamy fragrance-free cleanser", "Centella asiatica serum", "Ceramide moisturizer", "Mineral SPF 50"],
        "evening": ["Micellar water + cleanser lembut", "Serum peptide atau madecassoside", "Sleeping mask calming"],
        "ingredients": ["Ceramide", "Centella Asiatica", "Madecassoside", "Panthenol", "Allantoin"],
        "avoid": ["Fragrance", "Essential oil", "Physical scrub", "Retinol di awal", "Alkohol"],
    },
    {
        "id": "dry_aging",
        "cond": lambda m, c, r: m == "dry" and c == "aging",
        "type": "Kering & anti-aging",
        "desc": "Kulit kering dengan tanda penuaan. Butuh hidrasi intensif sekaligus stimulasi produksi kolagen.",
        "morning": ["Creamy cleanser", "Vitamin C + hyaluronic acid serum", "Rich ceramide moisturizer", "SPF 50"],
        "evening": ["Gentle cleanser", "Retinol (mulai 0.025%)", "Facial oil (rosehip/argan)", "Sleeping mask"],
        "ingredients": ["Retinol", "Peptide", "Hyaluronic Acid", "Ceramide", "Vitamin C", "Squalane"],
        "avoid": ["Harsh exfoliant", "Alkohol", "Air panas saat cuci muka"],
    },
    {
        "id": "dry_normal",
        "cond": lambda m, c, r: m == "dry",
        "type": "Kering",
        "desc": "Kulit membutuhkan hidrasi ekstra dan perlindungan barrier agar tidak semakin dehidrasi.",
        "morning": ["Creamy cleanser", "Hyaluronic acid serum", "Rich moisturizer", "SPF 30+"],
        "evening": ["Gentle cleanser", "Retinol ringan (2x/minggu)", "Facial oil", "Sleeping mask"],
        "ingredients": ["Hyaluronic Acid", "Shea Butter", "Ceramide", "Squalane", "Peptide"],
        "avoid": ["Alkohol", "Harsh exfoliant", "Air panas"],
    },
    {
        "id": "combo",
        "cond": lambda m, c, r: m == "combo",
        "type": "Kombinasi",
        "desc": "T-zone berminyak sementara area lain lebih kering atau normal. Butuh pendekatan balance tanpa memperparah salah satu area.",
        "morning": ["Balanced gel cleanser", "Niacinamide serum", "Lightweight moisturizer", "SPF 30+"],
        "evening": ["Gentle cleanser", "BHA toner di T-zone saja", "Retinol ringan", "Gel moisturizer"],
        "ingredients": ["Niacinamide", "Hyaluronic Acid", "Lactic Acid", "Green Tea Extract"],
        "avoid": ["Over-exfoliating area pipi", "Heavy oil di T-zone", "Skip moisturizer"],
    },
    {
        "id": "normal_aging",
        "cond": lambda m, c, r: m == "normal" and c == "aging",
        "type": "Normal & anti-aging",
        "desc": "Kulit seimbang dengan tanda penuaan awal. Ideal untuk preventive skincare.",
        "morning": ["Gentle cleanser", "Vitamin C serum", "Moisturizer ringan", "SPF 30+"],
        "evening": ["Cleanser", "Retinol (2–3x/minggu)", "Peptide moisturizer"],
        "ingredients": ["Vitamin C", "Retinol", "Peptide", "Niacinamide"],
        "avoid": ["Over-exfoliating", "Skip SPF"],
    },
    {
        "id": "normal",
        "cond": lambda m, c, r: True,
        "type": "Normal & seimbang",
        "desc": "Kulit dalam kondisi ideal. Fokus pada konsistensi dan pencegahan kerusakan jangka panjang.",
        "morning": ["Gentle cleanser", "Antioksidan serum", "Moisturizer ringan", "SPF 30+"],
        "evening": ["Cleanser", "Moisturizer"],
        "ingredients": ["Vitamin C", "Hyaluronic Acid", "Niacinamide", "SPF mineral"],
        "avoid": ["Produk terlalu banyak", "Skip SPF", "Over-exfoliating"],
    },
]


def forward_chain(main, concern, reaction):
    """Forward-chaining: evaluasi rule dari atas ke bawah, return match pertama."""
    for rule in KNOWLEDGE_BASE:
        if rule["cond"](main, concern, reaction):
            return {k: v for k, v in rule.items() if k not in ("id", "cond")}
    return {k: v for k, v in KNOWLEDGE_BASE[-1].items() if k not in ("id", "cond")}


# ════════════════════════════════════════════════════════════════
#  ROUTES
# ════════════════════════════════════════════════════════════════

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/social-battery", methods=["POST"])
def api_battery():
    data = request.get_json()
    try:
        hours, energy = run_fis(
            data["kelelahan"], data["durasi"],
            data["mood"], data["tidur"], data["introvert"]
        )

        if hours < 2:
            badge = "Battery hampir penuh"
            interps = [
                "Energi sosialmu masih sangat terjaga setelah interaksi ini.",
                "Durasi pendek atau suasana nyaman memperlambat drainase energi.",
                "Kamu siap untuk interaksi lagi dalam waktu dekat.",
            ]
            dos   = ["Istirahat ringan 15–30 menit", "Interaksi santai dengan orang dekat masih oke", "Tetap monitor kondisimu"]
            donts = ["Tidak ada batasan khusus saat ini"]
        elif hours < 6:
            badge = "Battery cukup"
            interps = [
                "Energi sosialmu berkurang berarti tapi masih dalam batas aman.",
                "Interaksi lanjutan masih bisa dilakukan dengan orang yang familiar.",
                "Situasi formal atau keramaian sebaiknya dihindari dulu.",
            ]
            dos   = ["Istirahat 30–60 menit", "Aktivitas solo yang menyenangkan", "Interaksi dengan orang sangat dekat oke"]
            donts = ["Acara sosial besar atau baru", "Pertemuan formal yang melelahkan", "Keramaian yang tidak perlu"]
        elif hours < 12:
            badge = "Battery rendah"
            interps = [
                "Interaksi tadi menguras cukup banyak energi sosialmu.",
                "Kombinasi durasi, tipe acara, dan kondisi fisikmu berkontribusi besar.",
                "Butuh waktu cukup untuk recharge sebelum siap bersosialisasi lagi.",
            ]
            dos   = ["Waktu sendirian yang cukup", "Aktivitas pasif — nonton, baca, dengar musik", "Tidur lebih awal malam ini", "Matikan notifikasi"]
            donts = ["Komitmen sosial baru hari ini", "Pertemuan formal", "Percakapan emosional yang berat"]
        else:
            badge = "Battery hampir habis"
            interps = [
                "Sistem FIS mendeteksi kombinasi faktor yang sangat menguras energi.",
                "Faktor introvert, kurang tidur, dan interaksi panjang berefek berlipat.",
                "Recovery serius diperlukan — ini respons alami, bukan kelemahan.",
            ]
            dos   = ["Isolasi sosial penuh jika memungkinkan", "Prioritaskan tidur dan istirahat total", "Komunikasi teks asinkron saja jika mendesak"]
            donts = ["Segala interaksi sosial baru", "Lingkungan ramai atau stimulatif", "Keputusan penting yang melibatkan orang lain"]

        return jsonify({"status": "ok", "hours": hours, "energy": energy,
                        "badge": badge, "interps": interps, "dos": dos, "donts": donts})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route("/api/skincare", methods=["POST"])
def api_skin():
    data = request.get_json()
    try:
        result = forward_chain(
            data.get("main", "normal"),
            data.get("concern", "acne"),
            data.get("reaction", "stable"),
        )
        return jsonify({"status": "ok", **result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)