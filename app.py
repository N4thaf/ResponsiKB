from flask import Flask, render_template, request, jsonify
import numpy as np

app = Flask(__name__)

def trimf(x, a, b, c):
    """Triangular membership function."""
    if x <= a or x >= c:
        return 0.0
    elif a < x <= b:
        return (x - a) / (b - a)
    else:
        return (c - x) / (c - b)


def trapmf(x, a, b, c, d):
    """Trapezoidal membership function."""
    if x <= a or x >= d:
        return 0.0
    elif b <= x <= c:
        return 1.0
    elif a < x < b:
        return (x - a) / (b - a)
    else:
        return (d - x) / (d - c)


def mf_kelelahan(val):
    return {
        'rendah': trapmf(val, 0, 0, 2, 4),
        'sedang': trimf(val, 3, 5, 7),
        'tinggi': trapmf(val, 6, 8, 10, 10),
    }

def mf_durasi(val):
    return {
        'singkat': trapmf(val, 0, 0, 1, 2),
        'sedang':  trimf(val, 1, 3, 6),
        'panjang': trapmf(val, 5, 7, 12, 12),
    }

def mf_mood(val):
    return {
        'buruk':  trapmf(val, 0, 0, 2, 4),
        'netral': trimf(val, 3, 5, 7),
        'baik':   trapmf(val, 6, 8, 10, 10),
    }

def mf_tidur(val):
    return {
        'kurang': trapmf(val, 0, 0, 4, 6),
        'cukup':  trimf(val, 5, 7, 8.5),
        'lebih':  trapmf(val, 8, 9, 10, 10),
    }

def mf_introvert(val):
    return {
        'ekstrovert': trapmf(val, 0, 0, 2, 4),
        'ambivert':   trimf(val, 3, 5, 7),
        'introvert':  trapmf(val, 6, 8, 10, 10),
    }


def defuzzify_centroid(activation_map, universe):
    """Defuzzifikasi metode centroid (Mamdani)."""
    def recovery_mf(label, x):
        if label == 'sangat_singkat': return trapmf(x, 0, 0, 1, 3)
        if label == 'singkat':        return trimf(x, 2, 4, 6)
        if label == 'sedang':         return trimf(x, 5, 8, 11)
        if label == 'panjang':        return trimf(x, 9, 13, 17)
        if label == 'sangat_panjang': return trapmf(x, 15, 19, 24, 24)
        return 0.0

    aggregated = np.zeros_like(universe, dtype=float)
    for label, strength in activation_map.items():
        if strength > 0:
            mf_vals = np.array([recovery_mf(label, x) for x in universe])
            aggregated = np.maximum(aggregated, np.minimum(strength, mf_vals))

    denom = np.sum(aggregated)
    if denom == 0:
        return 8.0  
    return float(np.sum(universe * aggregated) / denom)


def run_fis(kelelahan_val, durasi_val, mood_val, tidur_val, introvert_val):
    k = float(np.clip(kelelahan_val, 0, 10))
    d = float(np.clip(durasi_val,    0, 12))
    m = float(np.clip(mood_val,      0, 10))
    t = float(np.clip(tidur_val,     0, 10))
    i = float(np.clip(introvert_val, 0, 10))

    K = mf_kelelahan(k)
    D = mf_durasi(d)
    M = mf_mood(m)
    T = mf_tidur(t)
    I = mf_introvert(i)

    rules = {'sangat_singkat': 0.0, 'singkat': 0.0, 'sedang': 0.0,
             'panjang': 0.0, 'sangat_panjang': 0.0}

    def fire(output_label, *degrees):
        rules[output_label] = max(rules[output_label], min(degrees))

    fire('sangat_singkat', K['rendah'], D['singkat'], M['baik'])
    fire('sangat_singkat', K['rendah'], D['singkat'], I['ekstrovert'])
    fire('singkat',        K['rendah'], D['sedang'],  M['baik'], T['cukup'])
    fire('singkat',        K['rendah'], D['sedang'],  I['ambivert'])
    fire('sedang',         K['rendah'], D['panjang'], I['introvert'])
    fire('sedang',         K['rendah'], M['buruk'])
    fire('singkat',        K['rendah'], T['kurang'])

    fire('singkat',        K['sedang'], D['singkat'], M['baik'])
    fire('singkat',        K['sedang'], D['singkat'], I['ekstrovert'])
    fire('sedang',         K['sedang'], D['sedang'],  T['cukup'])
    fire('panjang',        K['sedang'], D['sedang'],  T['kurang'])
    fire('panjang',        K['sedang'], D['panjang'], I['introvert'])
    fire('sangat_panjang', K['sedang'], D['panjang'], M['buruk'])
    fire('panjang',        K['sedang'], M['buruk'],   T['kurang'])
    fire('sedang',         K['sedang'], I['ambivert'])

    fire('sedang',         K['tinggi'], D['singkat'], T['lebih'])
    fire('panjang',        K['tinggi'], D['singkat'], I['introvert'])
    fire('panjang',        K['tinggi'], D['sedang'])
    fire('sangat_panjang', K['tinggi'], D['panjang'])
    fire('sangat_panjang', K['tinggi'], T['kurang'])
    fire('sangat_panjang', K['tinggi'], M['buruk'])
    fire('sangat_panjang', K['tinggi'], I['introvert'], T['kurang'])

    fire('sangat_panjang', T['kurang'], M['buruk'],  I['introvert'])
    fire('sangat_singkat', T['lebih'],  M['baik'],   I['ekstrovert'])
    fire('singkat',        M['baik'],   T['cukup'],  I['ambivert'])

    universe = np.arange(0, 24.1, 0.1)
    recovery_hours = round(defuzzify_centroid(rules, universe), 1)

    energy_raw = 100 - (k * 8) - (d * 1.2) + (t * 1.5) + (m * 0.8)
    energy_pct = int(np.clip(energy_raw, 5, 95))

    return recovery_hours, energy_pct


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
    for rule in KNOWLEDGE_BASE:
        if rule["cond"](main, concern, reaction):
            return {k: v for k, v in rule.items() if k not in ("id", "cond")}
    return {k: v for k, v in KNOWLEDGE_BASE[-1].items() if k not in ("id", "cond")}


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
                "Recovery serius diperlukan.",
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