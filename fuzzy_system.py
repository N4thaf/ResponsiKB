import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class SocialBatteryFuzzy:
    def __init__(self):
        self._setup()
        self._rules()

    def _setup(self):
        self.kelelahan = ctrl.Antecedent(np.arange(0, 101, 1), 'kelelahan')
        self.tipe_acara = ctrl.Antecedent(np.arange(0, 101, 1), 'tipe_acara')
        self.durasi = ctrl.Antecedent(np.arange(0, 301, 1), 'durasi')
        self.tidur = ctrl.Antecedent(np.arange(0, 11, 1), 'kualitas_tidur')
        self.mood = ctrl.Antecedent(np.arange(0, 101, 1), 'mood')
        self.recovery = ctrl.Consequent(np.arange(0, 241, 1), 'recovery_time')

        self.kelelahan['rendah'] = fuzz.trimf(self.kelelahan.universe, [0, 0, 35])
        self.kelelahan['sedang'] = fuzz.trimf(self.kelelahan.universe, [20, 50, 80])
        self.kelelahan['tinggi'] = fuzz.trimf(self.kelelahan.universe, [65, 100, 100])

        self.tipe_acara['santai'] = fuzz.trimf(self.tipe_acara.universe, [0, 0, 40])
        self.tipe_acara['semi_formal'] = fuzz.trimf(self.tipe_acara.universe, [30, 50, 70])
        self.tipe_acara['formal'] = fuzz.trimf(self.tipe_acara.universe, [60, 100, 100])

        self.durasi['singkat'] = fuzz.trimf(self.durasi.universe, [0, 0, 60])
        self.durasi['sedang'] = fuzz.trimf(self.durasi.universe, [45, 150, 255])
        self.durasi['lama'] = fuzz.trimf(self.durasi.universe, [240, 300, 300])

        self.tidur['buruk'] = fuzz.trimf(self.tidur.universe, [0, 0, 5])
        self.tidur['cukup'] = fuzz.trimf(self.tidur.universe, [4, 7, 10])
        self.tidur['baik'] = fuzz.trimf(self.tidur.universe, [8, 10, 10])

        self.mood['rendah'] = fuzz.trimf(self.mood.universe, [0, 0, 35])
        self.mood['netral'] = fuzz.trimf(self.mood.universe, [25, 50, 75])
        self.mood['tinggi'] = fuzz.trimf(self.mood.universe, [65, 100, 100])

        self.recovery['tidak_perlu'] = fuzz.trimf(self.recovery.universe, [0, 0, 15])
        self.recovery['singkat'] = fuzz.trimf(self.recovery.universe, [10, 30, 60])
        self.recovery['sedang'] = fuzz.trimf(self.recovery.universe, [45, 90, 135])
        self.recovery['lama'] = fuzz.trimf(self.recovery.universe, [120, 180, 240])
        self.recovery['sangat_lama'] = fuzz.trimf(self.recovery.universe, [200, 240, 240])

    def _rules(self):
        r1 = ctrl.Rule(self.kelelahan['tinggi'] & self.tipe_acara['formal'] & self.durasi['lama'], self.recovery['sangat_lama'])
        r2 = ctrl.Rule(self.kelelahan['rendah'] & self.mood['tinggi'] & self.tipe_acara['santai'], self.recovery['tidak_perlu'])
        r3 = ctrl.Rule(self.tidur['buruk'] & self.kelelahan['sedang'], self.recovery['sedang'])
        r4 = ctrl.Rule(self.mood['rendah'] & self.durasi['lama'], self.recovery['lama'])
        r5 = ctrl.Rule(self.tipe_acara['formal'] & self.tidur['baik'], self.recovery['singkat'])
        r6 = ctrl.Rule(self.kelelahan['sedang'] & self.mood['netral'] & self.durasi['sedang'], self.recovery['sedang'])
        r7 = ctrl.Rule(self.tidur['baik'] & self.mood['tinggi'], self.recovery['singkat'])
        r8 = ctrl.Rule(self.durasi['singkat'] & self.tipe_acara['santai'], self.recovery['tidak_perlu'])
        r9 = ctrl.Rule(self.kelelahan['tinggi'] & self.mood['rendah'], self.recovery['sangat_lama'])
        r10 = ctrl.Rule(self.tidur['buruk'] & self.tipe_acara['formal'], self.recovery['lama'])
        r11 = ctrl.Rule(self.kelelahan['sedang'] & self.tipe_acara['semi_formal'], self.recovery['sedang'])
        r12 = ctrl.Rule(self.mood['netral'] & self.durasi['sedang'], self.recovery['sedang'])

        self.ctrl_sys = ctrl.ControlSystem([r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12])
        self.sim = ctrl.ControlSystemSimulation(self.ctrl_sys)

    def calculate(self, kelelahan, tipe_acara, durasi, tidur, mood):
        self.sim.input['kelelahan'] = kelelahan
        self.sim.input['tipe_acara'] = tipe_acara
        self.sim.input['durasi'] = durasi
        self.sim.input['kualitas_tidur'] = tidur
        self.sim.input['mood'] = mood
        self.sim.compute()
        val = self.sim.output['recovery_time']
        if val <= 15:
            cat, tip = "Tidak Perlu Recovery", "Energi kamu masih bagus! Lanjutkan aktivitasmu."
        elif val <= 60:
            cat, tip = "Recovery Singkat (30-60 menit)", "Istirahat sejenak: minum air, stretching, atau dengarkan musik."
        elif val <= 135:
            cat, tip = "Recovery Sedang (1-2 jam)", "Waktu untuk me-time: baca buku, meditasi, atau tidur siang."
        elif val <= 200:
            cat, tip = "Recovery Lama (2-3 jam)", "Istirahat yang cukup: hindari screen time, lakukan hobi yang menenangkan."
        else:
            cat, tip = "Recovery Sangat Lama (3-4 jam)", "Kamu butuh istirahat serius! Pertimbangkan untuk cancel rencana berikutnya."
        return {'recovery_time': round(val), 'category': cat, 'tips': tip}