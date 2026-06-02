import streamlit as st

SHARED_CSS = """
<style>
.section-header {
    font-family: 'Playfair Display', serif;
    font-size: 1.7rem;
    color: #0f2027;
    border-left: 4px solid #2c8faf;
    padding-left: .8rem;
    margin: 1.5rem 0 1rem;
}
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
.tab-card {
    background: white;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    box-shadow: 0 3px 18px rgba(44,83,100,.07);
    border: 1px solid rgba(44,83,100,.07);
}
</style>
"""

# ─────────────────────────────────────────────────────────────────────────────
#  DATA KONVERSI
# ─────────────────────────────────────────────────────────────────────────────

# Panjang — faktor ke meter
PANJANG = {
    "Kilometer (km)":    1e3,
    "Hektometer (hm)":   1e2,
    "Dekameter (dam)":   1e1,
    "Meter (m)":         1.0,
    "Desimeter (dm)":    1e-1,
    "Sentimeter (cm)":   1e-2,
    "Milimeter (mm)":    1e-3,
    "Mikrometer (µm)":   1e-6,
    "Nanometer (nm)":    1e-9,
}

# Massa — faktor ke gram
MASSA = {
    "Kilogram (kg)":    1e3,
    "Hektogram (hg)":   1e2,
    "Dekagram (dag)":   1e1,
    "Gram (g)":         1.0,
    "Desigram (dg)":    1e-1,
    "Sentigram (cg)":   1e-2,
    "Miligram (mg)":    1e-3,
    "Mikrogram (µg)":   1e-6,
    "Nanogram (ng)":    1e-9,
}

# Energi — faktor ke Joule
ENERGI = {
    "Joule (J)":            1.0,
    "Kilojoule (kJ)":       1e3,
    "Kalori (kal)":         4.184,
    "Kilokalori (kkal)":    4184.0,
    "Kilowatt-jam (kWh)":   3.6e6,
    "Elektronvolt (eV)":    1.60218e-19,
    "Erg":                  1e-7,
}

# Tekanan — faktor ke Pascal
TEKANAN = {
    "Pascal (Pa)":          1.0,
    "Kilopascal (kPa)":     1e3,
    "Bar":                  1e5,
    "Atmosfer (atm)":       101325.0,
    "mmHg (Torr)":          133.322,
    "cmHg":                 1333.22,
    "PSI":                  6894.76,
    "mbar":                 100.0,
}

# ─────────────────────────────────────────────────────────────────────────────
#  FUNGSI KONVERSI UMUM (faktor)
# ─────────────────────────────────────────────────────────────────────────────
def konversi_faktor(nilai, dari, ke, tabel):
    return nilai * tabel[dari] / tabel[ke]


# ─────────────────────────────────────────────────────────────────────────────
#  KONVERSI SUHU
# ─────────────────────────────────────────────────────────────────────────────
def konversi_suhu(nilai, dari, ke):
    # ke Celsius dulu
    if dari == "Celsius (°C)":
        c = nilai
    elif dari == "Fahrenheit (°F)":
        c = (nilai - 32) * 5 / 9
    elif dari == "Kelvin (K)":
        c = nilai - 273.15
    elif dari == "Réaumur (°Ré)":
        c = nilai * 5 / 4
    else:
        raise ValueError(f"Satuan tidak dikenal: {dari}")

    # dari Celsius ke tujuan
    if ke == "Celsius (°C)":
        return c
    elif ke == "Fahrenheit (°F)":
        return c * 9 / 5 + 32
    elif ke == "Kelvin (K)":
        return c + 273.15
    elif ke == "Réaumur (°Ré)":
        return c * 4 / 5
    else:
        raise ValueError(f"Satuan tidak dikenal: {ke}")


SUHU_SATUAN = ["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)", "Réaumur (°Ré)"]


# ─────────────────────────────────────────────────────────────────────────────
#  WIDGET KONVERSI GENERIK (faktor)
# ─────────────────────────────────────────────────────────────────────────────
def widget_faktor(tabel, prefix, satuan_nama):
    satuan_list = list(tabel.keys())
    col1, col2 = st.columns(2)
    with col1:
        dari = st.selectbox(f"Dari", satuan_list, key=f"{prefix}_dari")
    with col2:
        default_ke = satuan_list[1] if satuan_list[0] == dari else satuan_list[0]
        ke_idx = satuan_list.index(default_ke)
        ke = st.selectbox(f"Ke", satuan_list, index=ke_idx, key=f"{prefix}_ke")

    nilai = st.number_input(f"Nilai ({dari})", format="%.10g", key=f"{prefix}_val")

    if st.button(f"🔄 Konversi {satuan_nama}", key=f"btn_{prefix}"):
        if dari == ke:
            st.info("Satuan asal dan tujuan sama. Nilai tetap.")
            hasil = nilai
        else:
            hasil = konversi_faktor(nilai, dari, ke, tabel)
          # ✅ Simpan ke session_state
        st.session_state[f"{prefix}_hasil"] = (nilai, dari, hasil, ke)

    # ✅ Tampilkan hasil terakhir jika ada
    if f"{prefix}_hasil" in st.session_state:
        nilai, dari, hasil, ke = st.session_state[f"{prefix}_hasil"]
        st.markdown(f"""<div class="result-box">...</div>""",
                    unsafe_allow_html=True

        st.markdown(f"""
        <div class="result-box">
            <div class="result-label">Hasil</div>
            <div class="result-value">{hasil:,.8g}</div>
            <div style="margin-top:.4rem;font-size:.88rem;color:#4a7a90">
                {nilai:g} {dari} = {hasil:,.8g} {ke}
            </div>
        </div>
        """, unsafe_allow_html=True)
        return nilai, dari, hasil, ke
    return None


# ─────────────────────────────────────────────────────────────────────────────
#  WIDGET KONVERSI SUHU
# ─────────────────────────────────────────────────────────────────────────────
def widget_suhu():
    col1, col2 = st.columns(2)
    with col1:
        dari = st.selectbox("Dari", SUHU_SATUAN, key="suhu_dari")
    with col2:
        ke_options = [s for s in SUHU_SATUAN if s != dari]
        ke = st.selectbox("Ke", ke_options, key="suhu_ke")

    nilai = st.number_input(f"Nilai ({dari})", format="%.6g", key="suhu_val")

    if st.button("🔄 Konversi Suhu", key="btn_suhu"):
        hasil = konversi_suhu(nilai, dari, ke)
        st.markdown(f"""
        <div class="result-box">
            <div class="result-label">Hasil</div>
            <div class="result-value">{hasil:,.6g}</div>
            <div style="margin-top:.4rem;font-size:.88rem;color:#4a7a90">
                {nilai:g} {dari} = {hasil:,.6g} {ke}
            </div>
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  TABEL REFERENSI
# ─────────────────────────────────────────────────────────────────────────────
def tabel_referensi_suhu():
    rows = []
    bases = [0, 100, -40, 37, 273.15]
    for c in bases:
        rows.append({
            "Celsius": f"{c}",
            "Fahrenheit": f"{c*9/5+32:.2f}",
            "Kelvin": f"{c+273.15:.2f}",
            "Réaumur": f"{c*4/5:.2f}",
        })
    return rows


def tabel_panjang_ref():
    nilai_m = 1.0
    return {k: f"{nilai_m / v:.4g}" for k, v in PANJANG.items()}


# ─────────────────────────────────────────────────────────────────────────────
#  HALAMAN UTAMA
# ─────────────────────────────────────────────────────────────────────────────
def halaman_fisika():
    st.markdown(SHARED_CSS, unsafe_allow_html=True)
    st.markdown('<div class="hero-title" style="font-size:2.6rem">Konversi Fisika ⚛️</div>', unsafe_allow_html=True)
    st.markdown("Konversi berbagai besaran fisika: panjang, massa, suhu, energi, dan tekanan.", unsafe_allow_html=False)
    st.markdown('<hr style="border:none;border-top:1.5px solid rgba(44,83,100,.1);margin:1rem 0">', unsafe_allow_html=True)

    jenis = st.selectbox(
        "🔢 Pilih Jenis Konversi",
        ["📏 Panjang", "⚖️ Massa", "🌡️ Suhu", "⚡ Energi", "💨 Tekanan"],
        key="fisika_jenis",
    )

    st.markdown("---")

    # ── PANJANG ──────────────────────────────────────────────────────────────
    if jenis == "📏 Panjang":
        st.markdown('<div class="section-header">📏 Konversi Panjang</div>', unsafe_allow_html=True)
        st.caption("Dari Kilometer hingga Nanometer — 9 satuan tersedia.")
        with st.container():
            widget_faktor(PANJANG, "panjang", "Panjang")

        with st.expander("📋 Tabel Faktor Konversi Panjang (basis 1 meter)"):
            st.markdown("| Satuan | Setara dengan 1 m |")
            st.markdown("|--------|------------------|")
            for k, v in PANJANG.items():
                st.markdown(f"| {k} | `{1/v:.4g}` |")

    # ── MASSA ─────────────────────────────────────────────────────────────────
    elif jenis == "⚖️ Massa":
        st.markdown('<div class="section-header">⚖️ Konversi Massa</div>', unsafe_allow_html=True)
        st.caption("Dari Kilogram hingga Nanogram — 9 satuan tersedia.")
        widget_faktor(MASSA, "massa", "Massa")

        with st.expander("📋 Tabel Faktor Konversi Massa (basis 1 gram)"):
            st.markdown("| Satuan | Setara dengan 1 g |")
            st.markdown("|--------|------------------|")
            for k, v in MASSA.items():
                st.markdown(f"| {k} | `{1/v:.4g}` |")

    # ── SUHU ──────────────────────────────────────────────────────────────────
    elif jenis == "🌡️ Suhu":
        st.markdown('<div class="section-header">🌡️ Konversi Suhu</div>', unsafe_allow_html=True)
        st.caption("Kelvin · Celsius · Fahrenheit · Réaumur")
        widget_suhu()

        with st.expander("📋 Tabel Suhu Referensi"):
            st.markdown("""
| Titik | Celsius | Fahrenheit | Kelvin | Réaumur |
|-------|---------|-----------|--------|---------|
| Beku air | 0°C | 32°F | 273.15 K | 0°Ré |
| Didih air | 100°C | 212°F | 373.15 K | 80°Ré |
| Tubuh manusia | 37°C | 98.6°F | 310.15 K | 29.6°Ré |
| Titik −40 | −40°C | −40°F | 233.15 K | −32°Ré |
| Nol mutlak | −273.15°C | −459.67°F | 0 K | −218.52°Ré |
            """)
        with st.expander("📐 Rumus Konversi Suhu"):
            st.markdown("""
| Dari → Ke | Rumus |
|-----------|-------|
| °C → °F | (°C × 9/5) + 32 |
| °F → °C | (°F − 32) × 5/9 |
| °C → K | °C + 273.15 |
| K → °C | K − 273.15 |
| °C → °Ré | °C × 4/5 |
| °Ré → °C | °Ré × 5/4 |
            """)

    # ── ENERGI ────────────────────────────────────────────────────────────────
    elif jenis == "⚡ Energi":
        st.markdown('<div class="section-header">⚡ Konversi Energi</div>', unsafe_allow_html=True)
        st.caption("Joule · Kilojoule · Kalori · Kilokalori · kWh · eV · Erg")
        widget_faktor(ENERGI, "energi", "Energi")

        with st.expander("📋 Tabel Faktor Konversi Energi (basis 1 Joule)"):
            st.markdown("| Satuan | Nilai dalam Joule |")
            st.markdown("|--------|-----------------|")
            for k, v in ENERGI.items():
                st.markdown(f"| {k} | `{v:.4g} J` |")

    # ── TEKANAN ───────────────────────────────────────────────────────────────
    elif jenis == "💨 Tekanan":
        st.markdown('<div class="section-header">💨 Konversi Tekanan</div>', unsafe_allow_html=True)
        st.caption("Bar · mmHg · cmHg · Pascal · Atmosfer · PSI · kPa · mbar")
        widget_faktor(TEKANAN, "tekanan", "Tekanan")

        with st.expander("📋 Tabel Faktor Konversi Tekanan (basis 1 atm)"):
            atm_pa = TEKANAN["Atmosfer (atm)"]
            st.markdown("| Satuan | Setara 1 atm |")
            st.markdown("|--------|-------------|")
            for k, v in TEKANAN.items():
                st.markdown(f"| {k} | `{atm_pa/v:.4g}` |")
