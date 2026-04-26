KNOWLEDGE_BASE = [

    {
        "id": "oily_acne_sensitive",
        "cond": lambda m, c, r, e, a, u:
            m == "oily" and c == "acne" and (r == "irritate" or a == "fragrance"),
        "type": "Berminyak, berjerawat & sensitif",
        "desc": (
            "Kombinasi produksi sebum tinggi, jerawat aktif, dan kulit reaktif. "
            "Prioritas utama: kontrol minyak dengan bahan non-iritasi, hindari "
            "fragrance dan alkohol. Perlu pendekatan bertahap."
        ),
        "morning": [
            "Gentle sulfate-free foaming cleanser",
            "Niacinamide serum 5% (mulai rendah)",
            "Oil-free gel moisturizer fragrance-free",
            "Mineral sunscreen SPF 50",
        ],
        "evening": [
            "Micellar water + gentle cleanser",
            "Azelaic acid 10% (alternatif retinol yang lebih gentle)",
            "Centella asiatica calming serum",
            "Light gel moisturizer",
        ],
        "ingredients": ["Niacinamide", "Azelaic Acid", "Centella Asiatica", "Zinc PCA", "Panthenol"],
        "avoid": ["Fragrance", "Alkohol denat", "Essential oil", "Comedogenic oil", "BHA dosis tinggi awal"],
    },

    {
        "id": "oily_acne_humid",
        "cond": lambda m, c, r, e, a, u:
            m == "oily" and (c == "acne" or r == "breakout") and e == "humid",
        "type": "Berminyak & berjerawat (iklim lembap)",
        "desc": (
            "Kelembapan tinggi memperparah produksi sebum dan pori tersumbat. "
            "Di iklim tropis/lembap, routine harus lebih ringan dan fokus "
            "pada kontrol minyak sepanjang hari."
        ),
        "morning": [
            "Salicylic acid cleanser 1–2%",
            "Niacinamide + zinc serum",
            "Water-based gel moisturizer (minimal)",
            "SPF 50 oil-control formula",
        ],
        "evening": [
            "Double cleanse (wajib di iklim lembap)",
            "BHA toner 2%",
            "Retinol 0.025–0.05% (2–3x/minggu)",
            "Gel moisturizer tipis",
        ],
        "ingredients": ["Salicylic Acid", "Niacinamide", "Zinc PCA", "Retinol", "Tea Tree (konsentrasi rendah)"],
        "avoid": ["Heavy cream", "Facial oil apapun", "Produk oklusif", "Micellar water saja tanpa bilas"],
    },

    {
        "id": "oily_acne",
        "cond": lambda m, c, r, e, a, u:
            m == "oily" and (c == "acne" or r == "breakout"),
        "type": "Berminyak & berjerawat",
        "desc": (
            "Produksi sebum berlebih menyumbat pori dan memicu breakout. "
            "Fokus pada kontrol minyak, anti-inflamasi, dan pencegahan penyumbatan pori."
        ),
        "morning": [
            "Gentle foaming cleanser (salicylic acid 0.5–2%)",
            "Niacinamide serum 10%",
            "Oil-free non-comedogenic moisturizer",
            "SPF 30–50 ringan",
        ],
        "evening": [
            "Double cleanse (oil + gentle foam)",
            "BHA toner",
            "Retinol atau adapalene (2–3x/minggu)",
            "Light gel moisturizer",
        ],
        "ingredients": ["Salicylic Acid", "Niacinamide", "Benzoyl Peroxide", "Adapalene", "Zinc PCA"],
        "avoid": ["Heavy cream berlemak", "Coconut oil", "Alkohol konsentrasi tinggi", "Comedogenic oils"],
    },

    {
        "id": "oily_aging_mature",
        "cond": lambda m, c, r, e, a, u:
            m == "oily" and c == "aging" and u == "mature",
        "type": "Berminyak, anti-aging (kulit matang)",
        "desc": (
            "Kulit berminyak dengan tanda penuaan lebih lanjut. "
            "Dibutuhkan retinoid yang lebih kuat dan peptide intensif "
            "sambil tetap mengontrol sebum."
        ),
        "morning": [
            "Foaming cleanser",
            "Vitamin C 15–20% (L-ascorbic acid)",
            "Peptide serum",
            "Lightweight moisturizer",
            "SPF 50",
        ],
        "evening": [
            "Double cleanse",
            "Retinol 0.5–1% atau tretinoin (resep dokter)",
            "Hyaluronic acid serum",
            "Gel moisturizer",
        ],
        "ingredients": ["Vitamin C", "Retinol/Tretinoin", "Peptide", "Niacinamide", "AHA", "Coenzyme Q10"],
        "avoid": ["Heavy emollient", "Skip SPF", "Mineral oil", "Produk tanpa SPF di pagi hari"],
    },

    {
        "id": "oily_aging",
        "cond": lambda m, c, r, e, a, u:
            m == "oily" and c == "aging",
        "type": "Berminyak & anti-aging",
        "desc": (
            "Kulit berminyak dengan tanda penuaan dini. "
            "Butuh kontrol sebum sekaligus antioksidan dan booster kolagen."
        ),
        "morning": [
            "Foaming cleanser",
            "Vitamin C serum (L-ascorbic acid)",
            "Lightweight moisturizer",
            "SPF 30–50",
        ],
        "evening": [
            "Double cleanse",
            "Retinol (mulai rendah, naikkan bertahap)",
            "Gel moisturizer",
        ],
        "ingredients": ["Vitamin C", "Retinol", "Peptide", "Niacinamide", "AHA"],
        "avoid": ["Heavy emollient", "Skip SPF", "Mineral oil"],
    },

    {
        "id": "oily_stable",
        "cond": lambda m, c, r, e, a, u: m == "oily",
        "type": "Berminyak normal",
        "desc": (
            "Sebum tinggi tanpa masalah signifikan. "
            "Prioritas regulasi minyak dan menjaga pori tetap bersih."
        ),
        "morning": [
            "Gel cleanser ringan",
            "Hyaluronic acid serum",
            "Oil-free moisturizer",
            "SPF 30+",
        ],
        "evening": [
            "Double cleanse",
            "AHA/BHA toner (2–3x/minggu)",
            "Light moisturizer",
        ],
        "ingredients": ["Niacinamide", "Hyaluronic Acid", "AHA", "BHA", "Green Tea"],
        "avoid": ["Heavy oil", "Produk oklusif berat", "Comedogenic moisturizer"],
    },

    {
        "id": "dry_allergy",
        "cond": lambda m, c, r, e, a, u:
            m == "dry" and a in ("fragrance", "paraben", "both") and r == "irritate",
        "type": "Kering, sensitif & riwayat alergi",
        "desc": (
            "Kulit kering dengan skin barrier lemah dan riwayat alergi terhadap bahan tertentu. "
            "Gunakan produk dengan ingredient list minimal dan sudah teruji "
            "hypoallergenic. Patch test wajib sebelum produk baru."
        ),
        "morning": [
            "Fragrance-free, paraben-free creamy cleanser",
            "Madecassoside atau panthenol serum",
            "Ceramide + cholesterol moisturizer",
            "Physical (mineral) sunscreen SPF 50",
        ],
        "evening": [
            "Micellar water hypoallergenic + cleanser lembut",
            "Allantoin atau bisabolol serum (calming)",
            "Barrier repair cream (ceramide tinggi)",
            "Occlusif tipis seperti petrolatum jika sangat kering",
        ],
        "ingredients": ["Ceramide", "Cholesterol", "Panthenol", "Allantoin", "Madecassoside", "Squalane"],
        "avoid": ["Fragrance", "Paraben", "Essential oil", "Retinol (awal)", "AHA/BHA", "Pewarna buatan"],
    },

    {
        "id": "dry_sensitive",
        "cond": lambda m, c, r, e, a, u:
            m == "dry" and (c == "sensitive" or r == "irritate"),
        "type": "Kering & sensitif",
        "desc": (
            "Skin barrier lemah membuat kulit reaktif sekaligus kehilangan kelembapan. "
            "Pendekatan minimal dengan bahan calming dan barrier repair."
        ),
        "morning": [
            "Creamy fragrance-free cleanser",
            "Centella asiatica serum",
            "Ceramide moisturizer",
            "Mineral SPF 50",
        ],
        "evening": [
            "Micellar water + cleanser lembut",
            "Serum peptide atau madecassoside",
            "Sleeping mask calming",
        ],
        "ingredients": ["Ceramide", "Centella Asiatica", "Madecassoside", "Panthenol", "Allantoin"],
        "avoid": ["Fragrance", "Essential oil", "Physical scrub", "Retinol di awal", "Alkohol"],
    },

    {
        "id": "dry_aging_mature",
        "cond": lambda m, c, r, e, a, u:
            m == "dry" and c == "aging" and u == "mature",
        "type": "Kering & anti-aging (kulit matang)",
        "desc": (
            "Kulit kering dengan tanda penuaan signifikan. "
            "Butuh hidrasi berlapis dan stimulasi kolagen intensif."
        ),
        "morning": [
            "Creamy hydrating cleanser",
            "Vitamin C + ferulic acid serum",
            "Hyaluronic acid (multi-molecular)",
            "Rich peptide moisturizer",
            "SPF 50",
        ],
        "evening": [
            "Gentle cleansing balm",
            "Retinol 0.3–0.5% (atau bakuchiol jika sensitif)",
            "Ceramide + peptide serum",
            "Rich facial oil (rosehip/argan)",
            "Overnight sleeping mask",
        ],
        "ingredients": ["Retinol", "Peptide", "Hyaluronic Acid", "Ceramide", "Vitamin C", "Ferulic Acid", "Squalane", "Bakuchiol"],
        "avoid": ["Harsh exfoliant", "Alkohol", "Air panas", "Produk ringan yang tidak cukup melembapkan"],
    },

    {
        "id": "dry_aging",
        "cond": lambda m, c, r, e, a, u:
            m == "dry" and c == "aging",
        "type": "Kering & anti-aging",
        "desc": (
            "Kulit kering dengan tanda penuaan. "
            "Butuh hidrasi intensif sekaligus stimulasi produksi kolagen."
        ),
        "morning": [
            "Creamy cleanser",
            "Vitamin C + hyaluronic acid serum",
            "Rich ceramide moisturizer",
            "SPF 50",
        ],
        "evening": [
            "Gentle cleanser",
            "Retinol (mulai 0.025%)",
            "Facial oil (rosehip/argan)",
            "Sleeping mask",
        ],
        "ingredients": ["Retinol", "Peptide", "Hyaluronic Acid", "Ceramide", "Vitamin C", "Squalane"],
        "avoid": ["Harsh exfoliant", "Alkohol", "Air panas saat cuci muka"],
    },

    {
        "id": "dry_dry_climate",
        "cond": lambda m, c, r, e, a, u:
            m == "dry" and e == "dry",
        "type": "Kering (iklim kering/AC)",
        "desc": (
            "Kulit kering di lingkungan kering atau AC sepanjang hari mempercepat TEWL "
            "(transepidermal water loss). Dibutuhkan humektan berlapis dan oklusi."
        ),
        "morning": [
            "Hydrating gel cleanser",
            "Hyaluronic acid 3 layer (low/mid/high molecular)",
            "Ceramide + shea butter moisturizer",
            "SPF 30+",
        ],
        "evening": [
            "Gentle cleanser",
            "Glycerin toner",
            "Peptide + hyaluronic acid serum",
            "Rich cream moisturizer",
            "Facial oil sebagai sealant",
        ],
        "ingredients": ["Hyaluronic Acid", "Glycerin", "Ceramide", "Shea Butter", "Squalane", "Urea"],
        "avoid": ["Foam cleanser kuat", "Alkohol", "AHA terlalu sering", "Air panas"],
    },

    {
        "id": "dry_normal",
        "cond": lambda m, c, r, e, a, u: m == "dry",
        "type": "Kering",
        "desc": (
            "Kulit membutuhkan hidrasi ekstra dan perlindungan barrier "
            "agar tidak semakin dehidrasi."
        ),
        "morning": [
            "Creamy cleanser",
            "Hyaluronic acid serum",
            "Rich moisturizer",
            "SPF 30+",
        ],
        "evening": [
            "Gentle cleanser",
            "Retinol ringan (2x/minggu)",
            "Facial oil",
            "Sleeping mask",
        ],
        "ingredients": ["Hyaluronic Acid", "Shea Butter", "Ceramide", "Squalane", "Peptide"],
        "avoid": ["Alkohol", "Harsh exfoliant", "Air panas"],
    },

    {
        "id": "combo_acne",
        "cond": lambda m, c, r, e, a, u:
            m == "combo" and (c == "acne" or r == "breakout"),
        "type": "Kombinasi & berjerawat",
        "desc": (
            "T-zone berminyak dengan jerawat, area pipi lebih kering atau normal. "
            "Butuh pendekatan multi-zone: fokus BHA di T-zone, hidrasi di pipi."
        ),
        "morning": [
            "Balanced gel cleanser",
            "Niacinamide serum (seluruh wajah)",
            "Gel moisturizer tipis di T-zone, krim ringan di pipi",
            "SPF 30+ non-comedogenic",
        ],
        "evening": [
            "Gentle cleanser",
            "BHA toner di T-zone saja",
            "Spot treatment benzoyl peroxide di jerawat aktif",
            "Retinol tipis di T-zone (2–3x/minggu)",
            "Gel moisturizer",
        ],
        "ingredients": ["Niacinamide", "Salicylic Acid", "Benzoyl Peroxide", "Hyaluronic Acid", "Zinc PCA"],
        "avoid": ["Heavy cream di T-zone", "Comedogenic oil seluruh wajah", "Over-exfoliating area pipi"],
    },

    {
        "id": "combo_stable",
        "cond": lambda m, c, r, e, a, u: m == "combo",
        "type": "Kombinasi",
        "desc": (
            "T-zone berminyak sementara area lain lebih kering atau normal. "
            "Butuh pendekatan balance tanpa memperparah salah satu area."
        ),
        "morning": [
            "Balanced gel cleanser",
            "Niacinamide serum",
            "Lightweight moisturizer",
            "SPF 30+",
        ],
        "evening": [
            "Gentle cleanser",
            "BHA toner di T-zone saja",
            "Retinol ringan",
            "Gel moisturizer",
        ],
        "ingredients": ["Niacinamide", "Hyaluronic Acid", "Lactic Acid", "Green Tea Extract"],
        "avoid": ["Over-exfoliating area pipi", "Heavy oil di T-zone", "Skip moisturizer"],
    },

    {
        "id": "normal_aging_mature",
        "cond": lambda m, c, r, e, a, u:
            m == "normal" and c == "aging" and u == "mature",
        "type": "Normal & anti-aging (kulit matang)",
        "desc": (
            "Kulit normal dengan tanda penuaan yang sudah lebih jelas. "
            "Fokus pada stimulasi kolagen, antioksidan kuat, dan hidrasi mendalam."
        ),
        "morning": [
            "Gentle cleanser",
            "Vitamin C 15% + ferulic acid",
            "Peptide serum",
            "Moisturizer SPF 50",
        ],
        "evening": [
            "Cleanser",
            "Retinol 0.3–0.5%",
            "Hyaluronic acid serum",
            "Rich peptide moisturizer",
        ],
        "ingredients": ["Vitamin C", "Retinol", "Peptide", "Ferulic Acid", "Niacinamide", "Hyaluronic Acid"],
        "avoid": ["Over-exfoliating", "Skip SPF", "Produk tanpa antioksidan"],
    },

    {
        "id": "normal_aging",
        "cond": lambda m, c, r, e, a, u:
            m == "normal" and c == "aging",
        "type": "Normal & anti-aging",
        "desc": (
            "Kulit seimbang dengan tanda penuaan awal. "
            "Ideal untuk preventive skincare."
        ),
        "morning": [
            "Gentle cleanser",
            "Vitamin C serum",
            "Moisturizer ringan",
            "SPF 30+",
        ],
        "evening": [
            "Cleanser",
            "Retinol (2–3x/minggu)",
            "Peptide moisturizer",
        ],
        "ingredients": ["Vitamin C", "Retinol", "Peptide", "Niacinamide"],
        "avoid": ["Over-exfoliating", "Skip SPF"],
    },

    {
        "id": "normal_pigment",
        "cond": lambda m, c, r, e, a, u:
            m == "normal" and c == "pigment",
        "type": "Normal & hiperpigmentasi",
        "desc": (
            "Kulit normal dengan masalah flek atau hiperpigmentasi. "
            "Butuh brightening agent yang konsisten dan perlindungan UV ketat."
        ),
        "morning": [
            "Gentle cleanser",
            "Vitamin C + tranexamic acid serum",
            "Niacinamide moisturizer",
            "SPF 50 (wajib, flek memburuk tanpa SPF)",
        ],
        "evening": [
            "Cleanser",
            "Alpha arbutin serum",
            "Retinol (percepat cell turnover)",
            "Moisturizer",
        ],
        "ingredients": ["Vitamin C", "Tranexamic Acid", "Alpha Arbutin", "Niacinamide", "Kojic Acid", "Retinol"],
        "avoid": ["Skip SPF (fatal untuk pigmentasi)", "Panas berlebih", "Scrub kasar"],
    },

    {
        "id": "normal",
        "cond": lambda m, c, r, e, a, u: True,
        "type": "Normal & seimbang",
        "desc": (
            "Kulit dalam kondisi ideal. "
            "Fokus pada konsistensi dan pencegahan kerusakan jangka panjang."
        ),
        "morning": [
            "Gentle cleanser",
            "Antioksidan serum",
            "Moisturizer ringan",
            "SPF 30+",
        ],
        "evening": [
            "Cleanser",
            "Moisturizer",
        ],
        "ingredients": ["Vitamin C", "Hyaluronic Acid", "Niacinamide", "SPF mineral"],
        "avoid": ["Produk terlalu banyak", "Skip SPF", "Over-exfoliating"],
    },
]


def forward_chain(main, concern, reaction, environment, allergy, age_group):
    """
    Forward-chaining: evaluasi rule dari atas ke bawah, return match pertama.
    Parameter:
      main        : 'oily' | 'dry' | 'combo' | 'normal'
      concern     : 'acne' | 'aging' | 'dull' | 'sensitive' | 'pigment'
      reaction    : 'stable' | 'breakout' | 'irritate'
      environment : 'humid' | 'dry' | 'normal'
      allergy     : 'none' | 'fragrance' | 'paraben' | 'both'
      age_group   : 'young' | 'adult' | 'mature'
    """
    for rule in KNOWLEDGE_BASE:
        if rule["cond"](main, concern, reaction, environment, allergy, age_group):
            return {k: v for k, v in rule.items() if k not in ("id", "cond")}
    return {k: v for k, v in KNOWLEDGE_BASE[-1].items() if k not in ("id", "cond")}