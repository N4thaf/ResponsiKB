import numpy as np

# ════════════════════════════════════════════════════════════════
#  SISTEM FUZZY LOGIC — Social Battery Manager
#  Metode  : Mamdani
#  Input   : kelelahan, durasi, mood_awal, tidur, introvert_lvl,
#             tipe_interaksi, kebisingan
#  Output  : recovery (jam)
#  Defuzz  : Centroid
# ════════════════════════════════════════════════════════════════


def trimf(x, a, b, c):
    if x <= a or x >= c:
        return 0.0
    elif a < x <= b:
        return (x - a) / (b - a)
    else:
        return (c - x) / (c - b)


def trapmf(x, a, b, c, d):
    if x <= a or x >= d:
        return 0.0
    elif b <= x <= c:
        return 1.0
    elif a < x < b:
        return (x - a) / (b - a)
    else:
        return (d - x) / (d - c)


# ── Membership functions ────────────────────────────────────────

def mf_kelelahan(val):
    return {
        'rendah': trapmf(val, 0, 0, 2, 4),
        'sedang': trimf(val, 3, 5, 7),
        'tinggi': trapmf(val, 6, 8, 10, 10),
    }

def mf_durasi(val):
    return {
        'singkat':  trapmf(val, 0, 0, 1, 2),
        'sedang':   trimf(val, 1, 3, 6),
        'panjang':  trapmf(val, 5, 7, 12, 12),
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

def mf_tipe_interaksi(val):
    # 0=online, 5=tatap muka kenal, 10=publik/orang baru
    return {
        'online':     trapmf(val, 0, 0, 1, 3),
        'familiar':   trimf(val, 2, 5, 7),
        'publik':     trapmf(val, 6, 8, 10, 10),
    }

def mf_kebisingan(val):
    # 0=senyap, 10=sangat bising/ramai
    return {
        'tenang':  trapmf(val, 0, 0, 2, 4),
        'sedang':  trimf(val, 3, 5, 7),
        'bising':  trapmf(val, 6, 8, 10, 10),
    }


# ── Output MF ───────────────────────────────────────────────────

def recovery_mf(label, x):
    if label == 'sangat_singkat': return trapmf(x, 0, 0, 1, 3)
    if label == 'singkat':        return trimf(x, 2, 4, 6)
    if label == 'sedang':         return trimf(x, 5, 8, 11)
    if label == 'panjang':        return trimf(x, 9, 13, 17)
    if label == 'sangat_panjang': return trapmf(x, 15, 19, 24, 24)
    return 0.0


# ── Defuzzifikasi centroid ───────────────────────────────────────

def defuzzify_centroid(activation_map, universe):
    aggregated = np.zeros_like(universe, dtype=float)
    for label, strength in activation_map.items():
        if strength > 0:
            mf_vals = np.array([recovery_mf(label, x) for x in universe])
            aggregated = np.maximum(aggregated, np.minimum(strength, mf_vals))
    denom = np.sum(aggregated)
    if denom == 0:
        return 8.0
    return float(np.sum(universe * aggregated) / denom)


# ── Rule base & inferensi ────────────────────────────────────────

def run_fis(kelelahan_val, durasi_val, mood_val, tidur_val,
            introvert_val, tipe_val, kebisingan_val):

    k = float(np.clip(kelelahan_val,  0, 10))
    d = float(np.clip(durasi_val,     0, 12))
    m = float(np.clip(mood_val,       0, 10))
    t = float(np.clip(tidur_val,      0, 10))
    i = float(np.clip(introvert_val,  0, 10))
    tp = float(np.clip(tipe_val,      0, 10))
    kb = float(np.clip(kebisingan_val, 0, 10))

    K  = mf_kelelahan(k)
    D  = mf_durasi(d)
    M  = mf_mood(m)
    T  = mf_tidur(t)
    I  = mf_introvert(i)
    TP = mf_tipe_interaksi(tp)
    KB = mf_kebisingan(kb)

    rules = {
        'sangat_singkat': 0.0, 'singkat': 0.0, 'sedang': 0.0,
        'panjang': 0.0, 'sangat_panjang': 0.0
    }

    def fire(output_label, *degrees):
        rules[output_label] = max(rules[output_label], min(degrees))

    # ── Kelelahan rendah ────────────────────────────────────────
    fire('sangat_singkat', K['rendah'], D['singkat'], M['baik'])
    fire('sangat_singkat', K['rendah'], D['singkat'], I['ekstrovert'])
    fire('sangat_singkat', K['rendah'], TP['online'],   KB['tenang'])
    fire('singkat',        K['rendah'], D['sedang'],  M['baik'], T['cukup'])
    fire('singkat',        K['rendah'], D['sedang'],  I['ambivert'])
    fire('singkat',        K['rendah'], TP['familiar'], KB['sedang'])
    fire('sedang',         K['rendah'], D['panjang'], I['introvert'])
    fire('sedang',         K['rendah'], M['buruk'])
    fire('sedang',         K['rendah'], TP['publik'],  KB['bising'])
    fire('singkat',        K['rendah'], T['kurang'])

    # ── Kelelahan sedang ────────────────────────────────────────
    fire('singkat',        K['sedang'], D['singkat'], M['baik'])
    fire('singkat',        K['sedang'], D['singkat'], I['ekstrovert'])
    fire('singkat',        K['sedang'], TP['online'],  KB['tenang'])
    fire('sedang',         K['sedang'], D['sedang'],  T['cukup'])
    fire('sedang',         K['sedang'], I['ambivert'])
    fire('sedang',         K['sedang'], TP['familiar'], KB['sedang'])
    fire('panjang',        K['sedang'], D['sedang'],  T['kurang'])
    fire('panjang',        K['sedang'], D['panjang'], I['introvert'])
    fire('panjang',        K['sedang'], TP['publik'],  KB['sedang'])
    fire('panjang',        K['sedang'], M['buruk'],   T['kurang'])
    fire('sangat_panjang', K['sedang'], D['panjang'], M['buruk'])
    fire('sangat_panjang', K['sedang'], TP['publik'],  KB['bising'], I['introvert'])

    # ── Kelelahan tinggi ────────────────────────────────────────
    fire('sedang',         K['tinggi'], D['singkat'], T['lebih'])
    fire('sedang',         K['tinggi'], TP['online'],  KB['tenang'])
    fire('panjang',        K['tinggi'], D['singkat'], I['introvert'])
    fire('panjang',        K['tinggi'], D['sedang'])
    fire('panjang',        K['tinggi'], TP['familiar'], KB['bising'])
    fire('sangat_panjang', K['tinggi'], D['panjang'])
    fire('sangat_panjang', K['tinggi'], T['kurang'])
    fire('sangat_panjang', K['tinggi'], M['buruk'])
    fire('sangat_panjang', K['tinggi'], I['introvert'], T['kurang'])
    fire('sangat_panjang', K['tinggi'], TP['publik'],  KB['bising'])

    # ── Tipe interaksi & kebisingan dominan ─────────────────────
    fire('sangat_singkat', TP['online'],   KB['tenang'],  M['baik'])
    fire('singkat',        TP['online'],   KB['sedang'],  I['ambivert'])
    fire('sedang',         TP['familiar'], KB['bising'],  K['sedang'])
    fire('panjang',        TP['publik'],   KB['sedang'],  I['introvert'])
    fire('sangat_panjang', TP['publik'],   KB['bising'],  I['introvert'], T['kurang'])

    # ── Tidur & mood dominan ────────────────────────────────────
    fire('sangat_panjang', T['kurang'], M['buruk'],  I['introvert'])
    fire('sangat_singkat', T['lebih'],  M['baik'],   I['ekstrovert'])
    fire('singkat',        M['baik'],   T['cukup'],  I['ambivert'])
    fire('panjang',        T['kurang'], KB['bising'], I['introvert'])
    fire('sedang',         T['lebih'],  TP['online'], M['baik'])

    universe = np.arange(0, 24.1, 0.1)
    recovery_hours = round(defuzzify_centroid(rules, universe), 1)

    # Energy: formula heuristik diperluas
    energy_raw = (100
                  - (k  * 7.5)
                  - (d  * 1.2)
                  - (kb * 1.5)
                  - (tp * 1.0)
                  + (t  * 1.5)
                  + (m  * 0.8))
    energy_pct = int(np.clip(energy_raw, 5, 95))

    return recovery_hours, energy_pct