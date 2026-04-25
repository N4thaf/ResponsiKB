import streamlit as st
from fuzzy_system import SocialBatteryFuzzy
from expert_system import SkinExpertSystem

st.set_page_config(page_title="Wellness AI • Responsi KB", page_icon="✨", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
body, .stApp { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; background-color: #FAFAFA; }
h1, h2, h3, h4 { color: #1D1D1F; font-weight: 600; letter-spacing: -0.3px; }
.stTextInput>div>div>input, .stSelectbox>div>div, .stSlider>div>div>div, .stMultiselect>div>div { border-radius: 14px; border: 1px solid #E5E5EA; background: #FFFFFF; }
.stSlider>div>div>div>div { background-color: #FFB6C1; }
.card { background: #FFFFFF; border-radius: 20px; padding: 28px; box-shadow: 0 4px 24px rgba(0,0,0,0.04); border: 1px solid #F2F2F7; margin-bottom: 24px; }
.result-box { background: linear-gradient(135deg, #FFFFFF 0%, #FFF8F9 100%); border-radius: 20px; padding: 28px; box-shadow: 0 8px 32px rgba(255, 182, 193, 0.25); border: 1px solid #FFE4E8; margin-top: 24px; }
.stButton>button { background: linear-gradient(135deg, #FF8FA3 0%, #FF6B85 100%); color: white; border-radius: 14px; font-weight: 600; padding: 14px 28px; border: none; box-shadow: 0 4px 16px rgba(255, 107, 133, 0.3); transition: all 0.2s ease; }
.stButton>button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(255, 107, 133, 0.4); }
.badge { display: inline-block; background: #FFF0F3; color: #D6336C; padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; font-weight: 500; margin: 4px; }
.divider { height: 1px; background: #F2F2F7; margin: 20px 0; }
.header-gradient { background: linear-gradient(135deg, #FFF5F7 0%, #FFFFFF 100%); border-radius: 24px; padding: 32px; margin-bottom: 32px; border: 1px solid #FFE4E8; }
</style>
""", unsafe_allow_html=True)

fuzzy_sys = SocialBatteryFuzzy()
skin_sys = SkinExpertSystem()

st.markdown("""
<div class='header-gradient'>
    <h1 style='margin: 0 0 8px 0;'>✨ Wellness AI</h1>
    <p style='color: #86868B; margin: 0; font-size: 1.1rem;'>Responsi KB • Sistem Fuzzy & Sistem Pakar</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["🔋 Social Battery", "🧴 Skin Expert"])

with tab1:
    st.markdown("<div class='card'><h2>🔋 Social Battery Manager</h2><p style='color:#86868B; margin-top:8px;'>Sistem Fuzzy: Penentuan Durasi Pemulihan Energi Sosial</p></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        kelelahan = st.slider("Level Kelelahan", 0, 100, 50)
        durasi = st.slider("Durasi Interaksi (menit)", 0, 300, 120)
        tidur = st.slider("Kualitas Tidur (jam)", 0, 10, 7)
    with col2:
        tipe_acara = st.selectbox("Tipe Acara", ["Santai", "Semi-Formal", "Formal"])
        tipe_val = {"Santai": 20, "Semi-Formal": 50, "Formal": 85}[tipe_acara]
        mood = st.slider("Mood Saat Ini", 0, 100, 50)

    if st.button("Hitung Recovery Time", key="btn_fuzzy"):
        res = fuzzy_sys.calculate(kelelahan, tipe_val, durasi, tidur, mood)
        st.markdown(f"""
        <div class='result-box'>
            <h3>⏱️ Rekomendasi Recovery</h3>
            <div style='font-size: 3rem; font-weight: 700; color: #D6336C; margin: 12px 0;'>{res['recovery_time']} Menit</div>
            <div class='badge'>{res['category']}</div>
            <div class='divider'></div>
            <p style='color: #424245; line-height: 1.7; font-size: 1.05rem;'>💡 {res['tips']}</p>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.markdown("<div class='card'><h2>🧴 Skin Expert System</h2><p style='color:#86868B; margin-top:8px;'>Sistem Pakar: Identifikasi Jenis Kulit & Rekomendasi Skincare</p></div>", unsafe_allow_html=True)
    st.markdown("<div class='card'><h3>Pilih Ciri Kulit Kamu:</h3></div>", unsafe_allow_html=True)
    
    traits_map = {
        "Minyak berlebih di area T-zone": "oily_tzone",
        "Jerawat sering muncul": "frequent_breakouts",
        "Kulit terasa kencang setelah cuci muka": "tight_after_wash",
        "Ada bercak kering/bersisik": "dry_patches",
        "Wajah kemerahan/mudah iritasi": "redness",
        "Pori-pori terlihat besar": "visible_pores",
        "Kulit terasa perih saat pakai produk": "stinging",
        "Reaksi cepat terhadap produk baru": "reacts_to_products",
        "Kulit tampak kusam": "dull_skin",
        "Garis halus terlihat jelas": "fine_lines"
    }
    
    selected = st.multiselect("Centang yang sesuai", list(traits_map.keys()))
    selected_keys = [traits_map[t] for t in selected]

    if st.button("Analisis Kulit", key="btn_skin"):
        if not selected_keys:
            st.warning("Pilih minimal 1 ciri kulit.")
        else:
            res = skin_sys.identify(selected_keys)
            routine_html = "".join([f"<span class='badge'>{r}</span>" for r in res['routine']])
            st.markdown(f"""
            <div class='result-box'>
                <h3>✨ Hasil Analisis</h3>
                <div style='font-size: 2.5rem; font-weight: 700; color: #D6336C; margin: 12px 0;'>{res['type']}</div>
                <div class='badge'>Keyakinan: {res['confidence']}%</div>
                <div class='divider'></div>
                <h4 style='margin-bottom: 12px;'>🧴 Rutinitas yang Direkomendasikan:</h4>
                <div style='margin-bottom: 16px;'>{routine_html}</div>
                <p style='color: #424245; line-height: 1.7; font-size: 1.05rem;'>💡 {res['tips']}</p>
            </div>
            """, unsafe_allow_html=True)

st.markdown("<div style='text-align: center; color: #86868B; padding: 32px 0; font-size: 0.9rem;'>Made with ❤️ for Responsi KB</div>", unsafe_allow_html=True)