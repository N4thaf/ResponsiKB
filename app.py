from flask import Flask, render_template, request, jsonify
from sistemfuzzy import run_fis
from sistempakar import forward_chain

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/social-battery", methods=["POST"])
def api_battery():
    data = request.get_json()
    try:
        hours, energy = run_fis(
            kelelahan_val  = data["kelelahan"],
            durasi_val     = data["durasi"],
            mood_val       = data["mood"],
            tidur_val      = data["tidur"],
            introvert_val  = data["introvert"],
            tipe_val       = data["tipe"],       
            kebisingan_val = data["kebisingan"], 
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
                "Energi sosialmu berkurang, tapi masih dalam batas aman.",
                "Interaksi lanjutan masih bisa dilakukan dengan orang yang familiar.",
                "Situasi formal atau keramaian sebaiknya dihindari dulu.",
            ]
            dos   = ["Istirahat 30-60 menit", "Aktivitas solo yang menyenangkan", "Interaksi dengan orang sangat dekat oke"]
            donts = ["Acara sosial besar atau baru", "Pertemuan formal yang melelahkan", "Keramaian yang tidak perlu"]

        elif hours < 12:
            badge = "Battery rendah"
            interps = [
                "Interaksi tadi menguras cukup banyak energi sosialmu.",
                "Kombinasi durasi, tipe acara, dan kondisi lingkungan berkontribusi besar.",
                "Butuh waktu cukup untuk recharge sebelum siap bersosialisasi lagi.",
            ]
            dos   = ["Waktu sendirian yang cukup", "Aktivitas pasif, nonton, baca, dengar musik", "Tidur lebih awal malam ini", "Matikan notifikasi"]
            donts = ["Komitmen sosial baru hari ini", "Pertemuan formal", "Percakapan emosional yang berat"]

        else:
            badge = "Battery hampir habis"
            interps = [
                "Terdeteksi kombinasi faktor yang sangat menguras energi.",
                "Faktor introvert, lingkungan bising, dan interaksi panjang berefek berlipat.",
                "Recovery serius diperlukan.",
            ]
            dos   = ["Isolasi sosial penuh jika memungkinkan", "Prioritaskan tidur dan istirahat total", "Komunikasi teks asinkron saja jika mendesak"]
            donts = ["Segala interaksi sosial baru", "Lingkungan ramai atau stimulatif", "Keputusan penting yang melibatkan orang lain"]

        return jsonify({
            "status": "ok", "hours": hours, "energy": energy,
            "badge": badge, "interps": interps, "dos": dos, "donts": donts,
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


@app.route("/api/skincare", methods=["POST"])
def api_skin():
    data = request.get_json()
    try:
        result = forward_chain(
            main        = data.get("main",        "normal"),
            concern     = data.get("concern",     "acne"),
            reaction    = data.get("reaction",    "stable"),
            environment = data.get("environment", "normal"),
            allergy     = data.get("allergy",     "none"),
            age_group   = data.get("age_group",   "adult"),
        )
        return jsonify({"status": "ok", **result})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)