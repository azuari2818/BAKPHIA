import streamlit as st
import random
from konversi_kimia import halaman_kimia
from konversi_fisika import halaman_fisika

# ─── Konfigurasi halaman ────────────────────────────────────────────────────
st.set_page_config(
    page_title="BAKPHIA – Bantuan Konversi Fisika & Kimia",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS global ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0f2027, #203a43, #2c5364);
    border-right: 1px solid rgba(255,255,255,0.08);
}
[data-testid="stSidebar"] * { color: #e0f4ff !important; }
[data-testid="stSidebar"] .stRadio label { font-size: 1rem; }

/* ── Main area ── */
[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 0%, #e8f4f8 0%, #f5fafc 60%, #eef6f9 100%);
}

/* ── Hero title ── */
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3.6rem;
    font-weight: 900;
    background: linear-gradient(135deg, #0f2027 0%, #2c5364 50%, #1a6e8e 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.1;
    margin-bottom: .3rem;
}
.hero-sub {
    font-size: 1.1rem;
    color: #4a7a90;
    letter-spacing: .08em;
    text-transform: uppercase;
    font-weight: 500;
}

/* ── Cards ── */
.card {
    background: white;
    border-radius: 16px;
    padding: 1.6rem 1.8rem;
    box-shadow: 0 4px 24px rgba(44,83,100,.08);
    border: 1px solid rgba(44,83,100,.07);
    margin-bottom: 1rem;
}
.card h3 {
    font-family: 'Playfair Display', serif;
    color: #0f2027;
    margin-bottom: .5rem;
    font-size: 1.3rem;
}
.card p { color: #456b7a; line-height: 1.7; margin: 0; }

/* ── Jokes card ── */
.jokes-card {
    background: linear-gradient(135deg, #203a43, #2c5364);
    border-radius: 16px;
    padding: 1.8rem 2rem;
    color: white;
    text-align: center;
    box-shadow: 0 8px 32px rgba(15,32,39,.25);
    margin-top: .5rem;
}
.jokes-card .label {
    font-size: .78rem;
    letter-spacing: .15em;
    text-transform: uppercase;
    color: #7ecfea;
    margin-bottom: .6rem;
}
.jokes-card .joke-text {
    font-family: 'Playfair Display', serif;
    font-size: 1.25rem;
    line-height: 1.6;
    color: #e8f8ff;
}
.jokes-card .punchline {
    margin-top: .8rem;
    font-size: .95rem;
    color: #a8e6f5;
    font-style: italic;
}

/* ── Section header ── */
.section-header {
    font-family: 'Playfair Display', serif;
    font-size: 1.7rem;
    color: #0f2027;
    border-left: 4px solid #2c8faf;
    padding-left: .8rem;
    margin: 1.5rem 0 1rem;
}

/* ── Result box ── */
.result-box {
    background: linear-gradient(135deg, #e8f8ff, #d0effa);
    border: 1.5px solid #7ecfea;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    text-align: center;
    margin-top: .8rem;
}
.result-box .result-label {
    font-size: .8rem;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: #2c8faf;
    margin-bottom: .3rem;
}
.result-box .result-value {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    color: #0f2027;
    font-weight: 700;
}
.result-box .result-unit {
    font-size: 1rem;
    color: #4a9db5;
    margin-left: .3rem;
}

/* ── Divider ── */
hr.styled { border: none; border-top: 1.5px solid rgba(44,83,100,.1); margin: 1.5rem 0; }

/* ── Streamlit widget overrides ── */
.stSelectbox label, .stNumberInput label, .stRadio label {
    font-weight: 500; color: #1e3d4a !important;
}
.stButton > button {
    background: linear-gradient(135deg, #203a43, #2c5364);
    color: white;
    border: none;
    border-radius: 10px;
    padding: .55rem 2rem;
    font-size: 1rem;
    font-weight: 500;
    transition: opacity .2s;
    width: 100%;
}
.stButton > button:hover { opacity: .88; }
</style>
""", unsafe_allow_html=True)

# ─── Jokes database ─────────────────────────────────────────────────────────
JOKES = [
    {"q": "Kenapa atom tidak bisa dipercaya?", "a": "Karena mereka membentuk segalanya! 😄"},
    {"q": "Apa yang dikatakan ion positif kepada ion negatif?", "a": "Kamu selalu menarikku! 🧲"},
    {"q": "Kenapa oksigen dan magnesium bersahabat?", "a": "Karena mereka itu OMg! 😲"},
    {"q": "Apakah lelucon tentang kimia ini baik?", "a": "Saya tunggu reaksimu... 😏"},
    {"q": "Dua atom berjalan. Satu berkata: 'Aku kehilangan elektron.'", "a": "Yang lain: 'Kamu yakin?' — 'Ya, aku positif!' ⚡"},
    {"q": "Kenapa ilmuwan tidak bisa dipercaya?", "a": "Karena mereka terlalu banyak teori! 🔬"},
    {"q": "Apa nama unsur kimia yang paling romantis?", "a": "Europium (Eu)! Karena penuh EU-foria 💕"},
    {"q": "H2O adalah air. Apa itu H2O2?", "a": "Air lagi... tapi di selokan! 😂"},
    {"q": "Mengapa kimia organik sangat sulit?", "a": "Karena orang yang belajarnya sering alCOHOL-ic! 🍺"},
    {"q": "Apa kata neutron saat akan membeli sesuatu?", "a": "'Berapa harganya?' — 'Untuk kamu? Tidak ada muatan!' ⚛️"},
    {"q": "Kenapa pH larutan basa selalu tenang?", "a": "Karena mereka tidak pernah asam hati! 🙂"},
    {"q": "Unsur apa yang paling sombong?", "a": "Gold (Au) — karena selalu Au-some! ✨"},
    {"q": "Apa yang dikatakan H₂SO₄ kepada Ba(OH)₂?", "a": "'Kita bisa netral, kok!' 🧪"},
    {"q": "Kenapa elektron tidak pernah tersesat?", "a": "Karena mereka selalu tahu orbitnya! 🌀"},
    {"q": "Bagaimana cara ilmuwan menyegarkan napas?", "a": "Dengan minum Helium — biar keren! He-he! 😆"}, 
    {"q": "Kenapa natrium (Na) selalu jadi sahabat yang baik?", "a": "Karena dia sangat reaktif kalau diajak jalan-jalan! 💥"},
    {"q": "Apa sebutan untuk alkana yang sedang jatuh cinta?", "a": "Alkana-kenanglah daku di dalam hatimu... 🥰"},
    {"q": "Kenapa ikatan kovalen adalah hubungan ideal?", "a": "Karena prinsip mereka adalah saling berbagi (elektron) secara adil! 🤝"},
    {"q": "Apa yang dikatakan asam klorida (HCl) saat mau berpisah dengan NaOH?", "a": "Sampai jumpa di titik ekivalen, ya! 💧"},
    {"q": "Kenapa unsur halogen (Golongan VIIA) sangat agresif?", "a": "Karena mereka kurang satu elektron lagi untuk mencapai kebahagiaan sempurna (oktet)! 💍"},
    {"q": "Kenapa es batu mengapung di atas air?", "a": "Biar dia bisa pamer kalau densitasnya lebih rendah! 🧊"},
    {"q": "Kenapa gas mulia (Golongan VIIIA) selalu jomblo?", "a": "Karena mereka sudah stabil dan enggan berikatan dengan siapa pun! 🛑"},
    {"q": "Apa bedanya ahli kimia organik dengan orang biasa saat melihat cincin?", "a": "Orang biasa melihat berlian, ahli kimia melihat struktur Benzena! 💍⬡"},
    {"q": "Kenapa indikator PP (Fenolftalein) suka panik kalau ketemu basa?", "a": "Karena mukanya langsung berubah jadi merah muda merona! 🌸"},
    {"q": "Apa hidangan penutup favorit para laboran?", "a": "Kue tart-rat (Tartrate)! 🍰"},
    {"q": "Kenapa reaksi eksotermik sangat populer di musim dingin?", "a": "Karena mereka selalu membagikan kehangatan (kalor) ke lingkungan sekitar! 🔥"},
    {"q": "Unsur apa yang paling suka memasak?", "a": "Tembaga (Cu), karena dia adalah 'Cu-linery' sejati! 🍳"},
    {"q": "Kenapa partikel koloid tidak pernah jatuh ke dasar?", "a": "Karena mereka sibuk nge-dance pakai Gerak Brown! 🕺"},
    {"q": "Apa yang dikatakan atom karbon saat bertemu tiga atom hidrogen?", "a": "Aku masih punya satu tangan kosong untuk menggandengmu! ⚛️"},
    {"q": "Kenapa garam dapur (NaCl) tidak pernah takut hancur?", "a": "Karena kisi kristalnya punya ikatan ionik yang sangat kuat! 💎"},
    {"q": "Apa mata pelajaran favorit molekul polar?", "a": "Geografi, karena mereka suka sekali membahas tentang kutub! 🧭"},
    {"q": "Kenapa larutan penyangga (buffer) sangat penyabar?", "a": "Karena seberapa besar pun tekanan (asam/basa) dari luar, mereka tetap berusaha mempertahankan pH diri! 🧘"},
    {"q": "Kenapa para ilmuwan tidak suka minum kopi di gelas beaker?", "a": "Karena takarannya terlalu presisi, bikin kopi kurang santai! 🧪"},
    {"q": "Bagaimana cara mendeteksi apakah seseorang itu ahli kimia?", "a": "Minta dia mengeja kata 'Copper'. Kalau dia jawab 'Cu', berarti fix! 🔬"},
    {"q": "Kenapa katalis tidak pernah masuk hitungan hasil akhir?", "a": "Karena tugas dia cuma mempercepat hubungan, lalu pergi tanpa minta imbalan... 🏃‍♂️"}
]

# ─── Sidebar navigasi ────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚗️ **BAKPHIA**")
    st.markdown("*Bantuan Konversi Fisika & Kimia*")
    st.markdown("---")
    menu = st.radio(
        "Navigasi",
        ["🏠 Beranda", "🧪 Konversi Kimia", "⚛️ Konversi Fisika"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown(
        "<small style='color:#7ecfea'>Dikembangkan untuk memudahkan<br>konversi satuan sains.</small>",
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────────────────────────────────────
#  HALAMAN BERANDA
# ─────────────────────────────────────────────────────────────────────────────
if menu == "🏠 Beranda":
    # Header
    st.markdown('<div class="hero-title">BAKPHIA</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">Bantuan Konversi Fisika &amp; Kimia</div>', unsafe_allow_html=True)
    st.markdown('<hr class="styled">', unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2], gap="large")

    with col1:
        st.markdown('<div class="section-header">Tentang BAKPHIA</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <h3>🎯 Tujuan</h3>
            <p>BAKPHIA hadir sebagai alat bantu konversi satuan yang dirancang khusus untuk
            pelajar, mahasiswa, dan praktisi di bidang Fisika dan Kimia. Tujuan utama kami adalah
            menyederhanakan proses konversi satuan yang sering memakan waktu dan rentan
            terhadap kesalahan perhitungan manual.</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <h3>✅ Manfaat</h3>
            <p>
            🔬 <b>Konversi Kimia</b> — Ubah satuan konsentrasi larutan (Molaritas, Normalitas,
            Molalitas, %b/v, %b/b, ppm, ppb) dengan cepat dan akurat.<br><br>
            🔭 <b>Konversi Fisika</b> — Konversi berbagai besaran fisika: panjang, massa, suhu,
            energi, dan tekanan dalam satu platform terintegrasi.<br><br>
            ⚡ <b>Hemat Waktu</b> — Tidak perlu lagi menghitung manual atau mencari faktor
            konversi satu per satu.<br><br>
            📱 <b>Mudah Digunakan</b> — Antarmuka intuitif yang bisa diakses kapan saja dan
            di mana saja.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <h3>🚀 Cara Penggunaan</h3>
            <p>Pilih menu <b>Konversi Kimia</b> atau <b>Konversi Fisika</b> pada panel navigasi
            di sebelah kiri. Masukkan nilai yang ingin dikonversi, pilih satuan asal dan satuan
            tujuan, lalu klik <b>Konversi</b> untuk melihat hasilnya secara instan.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-header">Jokes Kimia 🧪</div>', unsafe_allow_html=True)

        # Random joke — pakai session_state agar konsisten per sesi tapi bisa di-refresh
        if "joke_idx" not in st.session_state:
            st.session_state.joke_idx = random.randint(0, len(JOKES) - 1)

        joke = JOKES[st.session_state.joke_idx]
        st.markdown(f"""
        <div class="jokes-card">
            <div class="label">⚗️ Chemistry Joke of the Day</div>
            <div class="joke-text">{joke['q']}</div>
            <div class="punchline">{joke['a']}</div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🎲 Jokes Lain!", key="new_joke"):
            st.session_state.joke_idx = random.randint(0, len(JOKES) - 1)
            st.rerun()
        ] 
        st.markdown("""
        <div class="card" style="margin-bottom:.6rem">
            <h3 style="font-size:1rem">🧪 Konversi Kimia</h3>
            <p style="font-size:.88rem">Normalitas &middot; Molaritas &middot; Molalitas &middot; %b/v &middot; %b/b &middot; ppm &middot; ppb</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="card">
            <h3 style="font-size:1rem">🔮 Konversi Fisika</h3>
            <p style="font-size:.88rem">Panjang &middot; Massa &middot; Suhu &middot; Energi &middot; Tekanan</p>
        </div>
        """, unsafe_allow_html=True)

def tampilkan_kreator():
    st.markdown("---")
    st.markdown("""
        <div style="text-align:center; margin-bottom: 1rem;">
            <p style="font-size:12px; color:#888; letter-spacing:0.08em; text-transform:uppercase; margin:0 0 4px;">
                Tim Pengembang
            </p>
            <p style="font-size:20px; font-weight:500; margin:0;">
                Kreator Aplikasi
            </p>
        </div>
    """, unsafe_allow_html=True)

    kreator = [
        {"nama": "Dzahwan Alamsyah",       "nim": "2560616", "inisial": "DA", "warna_bg": "#E6F1FB", "warna_teks": "#0C447C"},
        {"nama": "Irma Dwi Anggreani",      "nim": "2560645", "inisial": "ID", "warna_bg": "#E1F5EE", "warna_teks": "#0F6E56"},
        {"nama": "Muhammad Azuari",         "nim": "2560677", "inisial": "MA", "warna_bg": "#FAEEDA", "warna_teks": "#854F0B"},
        {"nama": "Nasya Nur Zafira",        "nim": "2560711", "inisial": "NN", "warna_bg": "#EEEDFE", "warna_teks": "#534AB7"},
        {"nama": "Shafa Amalia Shaleha M.", "nim": "2560777", "inisial": "SA", "warna_bg": "#FBEAF0", "warna_teks": "#993556"},
    ]

    cols = st.columns(len(kreator))
    for col, k in zip(cols, kreator):
        with col:
            st.markdown(f"""
                <div style="
                    background: white;
                    border: 0.5px solid #e0e0e0;
                    border-radius: 12px;
                    padding: 1rem;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    gap: 8px;
                    text-align: center;
                ">
                    <div style="
                        width: 48px; height: 48px;
                        border-radius: 50%;
                        background: {k['warna_bg']};
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 15px;
                        font-weight: 500;
                        color: {k['warna_teks']};
                    ">{k['inisial']}</div>
                    <div>
                        <p style="font-size:13px; font-weight:500; margin:0 0 2px; color:#111;">{k['nama']}</p>
                        <p style="font-size:12px; color:#888; margin:0;">{k['nim']}</p>
                    </div>
                </div>
            """, unsafe_allow_html=True)
# ─────────────────────────────────────────────────────────────────────────────
#  HALAMAN KONVERSI KIMIA
# ─────────────────────────────────────────────────────────────────────────────
elif menu == "🧪 Konversi Kimia":
    halaman_kimia()

# ─────────────────────────────────────────────────────────────────────────────
#  HALAMAN KONVERSI FISIKA
# ─────────────────────────────────────────────────────────────────────────────
elif menu == "⚛️ Konversi Fisika":
    halaman_fisika()
