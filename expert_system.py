class SkinExpertSystem:
    def __init__(self):
        self.skin_types = {
            'Oily': {'traits': ['oily_tzone', 'visible_pores', 'frequent_breakouts'], 'routine': ['Gel Cleanser', 'Oil-Free Moisturizer', 'Salicylic Acid', 'Matte Sunscreen'], 'tips': 'Hindari produk berbasis minyak. Fokus pada kontrol sebum dan eksfoliasi ringan.'},
            'Dry': {'traits': ['tight_after_wash', 'dry_patches', 'dull_skin', 'fine_lines'], 'routine': ['Cream Cleanser', 'Hyaluronic Acid', 'Ceramide Moisturizer', 'Facial Oil'], 'tips': 'Gunakan pelembab bertekstur kaya. Hindari alkohol, fragrance, dan scrub kasar.'},
            'Combination': {'traits': ['oily_tzone', 'dry_cheeks', 'visible_pores', 'occasional_breakouts'], 'routine': ['Gentle Foam Cleanser', 'Light Moisturizer', 'Niacinamide', 'Lightweight Sunscreen'], 'tips': 'Rawat area berminyak dan kering secara berbeda. Gunakan produk balancing.'},
            'Sensitive': {'traits': ['redness', 'stinging', 'reacts_to_products', 'dry_patches'], 'routine': ['Micellar Water', 'Soothing Moisturizer', 'Centella Asiatica', 'Mineral Sunscreen'], 'tips': 'Pilih produk fragrance-free & hypoallergenic. Selalu lakukan patch test.'},
            'Normal': {'traits': ['balanced_oil', 'rare_breakouts', 'smooth_texture', 'even_tone'], 'routine': ['Gentle Cleanser', 'Light Moisturizer', 'Vitamin C', 'Broad Spectrum Sunscreen'], 'tips': 'Jaga keseimbangan barrier kulit. Rutinitas sederhana sudah sangat cukup.'}
        }

    def identify(self, traits):
        scores = {}
        for stype, data in self.skin_types.items():
            score = sum(1 for t in data['traits'] if t in traits)
            if score > 0:
                scores[stype] = score
        if not scores:
            return {'type': 'Normal', 'confidence': 60, 'routine': ['Gentle Cleanser', 'Light Moisturizer', 'Sunscreen'], 'tips': 'Kulit tampak seimbang. Pertahankan rutinitas dasar & proteksi UV.'}
        best_type = max(scores, key=scores.get)
        confidence = int((scores[best_type] / len(self.skin_types[best_type]['traits'])) * 100)
        confidence = min(confidence, 98)
        return {'type': best_type, 'confidence': confidence, 'routine': self.skin_types[best_type]['routine'], 'tips': self.skin_types[best_type]['tips']}