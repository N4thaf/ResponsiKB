import numpy as np

class SocialBatteryFuzzy:
    def _trimf(self, x, a, b, c):
        return np.maximum(0, np.minimum((x - a) / (b - a + 1e-10), (c - x) / (c - b + 1e-10)))
    
    def _calculate(self, kelelahan, tipe_acara, durasi, tidur, mood):
        kelelahan_rendah = self._trimf(kelelahan, 0, 0, 35)
        kelelahan_sedang = self._trimf(kelelahan, 20, 50, 80)
        kelelahan_tinggi = self._trimf(kelelahan, 65, 100, 100)
        
        acara_santai = self._trimf(tipe_acara, 0, 0, 40)
        acara_semi = self._trimf(tipe_acara, 30, 50, 70)
        acara_formal = self._trimf(tipe_acara, 60, 100, 100)
        
        durasi_singkat = self._trimf(durasi, 0, 0, 60)
        durasi_sedang = self._trimf(durasi, 45, 150, 255)
        durasi_lama = self._trimf(durasi, 240, 300, 300)
        
        tidur_buruk = self._trimf(tidur, 0, 0, 5)
        tidur_cukup = self._trimf(tidur, 4, 7, 10)
        tidur_baik = self._trimf(tidur, 8, 10, 10)
        
        mood_rendah = self._trimf(mood, 0, 0, 35)
        mood_netral = self._trimf(mood, 25, 50, 75)
        mood_tinggi = self._trimf(mood, 65, 100, 100)
        
        recovery_centers = {'tidak_perlu': 5, 'singkat': 35, 'sedang': 90, 'lama': 180, 'sangat_lama': 220}
        
        rules = [
            (min(kelelahan_tinggi, acara_formal, durasi_lama), recovery_centers['sangat_lama']),
            (min(kelelahan_rendah, mood_tinggi, acara_santai), recovery_centers['tidak_perlu']),
            (min(tidur_buruk, kelelahan_sedang), recovery_centers['sedang']),
            (min(mood_rendah, durasi_lama), recovery_centers['lama']),
            (min(acara_formal, tidur_baik), recovery_centers['singkat']),
            (min(kelelahan_sedang, mood_netral, durasi_sedang), recovery_centers['sedang']),
            (min(tidur_baik, mood_tinggi), recovery_centers['singkat']),
            (min(durasi_singkat, acara_santai), recovery_centers['tidak_perlu']),
            (min(kelelahan_tinggi, mood_rendah), recovery_centers['sangat_lama']),
            (min(tidur_buruk, acara_formal), recovery_centers['lama']),
        ]
        
        numerator = sum(w * v for w, v in rules if w > 0)
        denominator = sum(w for w, _ in rules if w > 0)
        recovery_time = numerator / denominator if denominator > 0 else 60
        
        if recovery_time <= 15:
            category, tips = "Tidak Perlu Recovery", "Energi kamu masih bagus! Lanjutkan aktivitasmu."
        elif recovery_time <= 60:
            category, tips = "Recovery Singkat (30-60 menit)", "Istirahat sejenak: minum air, stretching, atau dengarkan musik."
        elif recovery_time <= 135:
            category, tips = "Recovery Sedang (1-2 jam)", "Waktu untuk me-time: baca buku, meditasi, atau tidur siang."
        elif recovery_time <= 200:
            category, tips = "Recovery Lama (2-3 jam)", "Istirahat yang cukup: hindari screen time, lakukan hobi yang menenangkan."
        else:
            category, tips = "Recovery Sangat Lama (3-4 jam)", "Kamu butuh istirahat serius! Pertimbangkan untuk cancel rencana berikutnya."
        
        return {'recovery_time': round(recovery_time), 'category': category, 'tips': tips}
    
    def calculate(self, kelelahan, tipe_acara, durasi, tidur, mood):
        return self._calculate(kelelahan, tipe_acara, durasi, tidur, mood)