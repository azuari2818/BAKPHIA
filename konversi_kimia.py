import streamlit as st

# ─── Shared CSS helper (injected once per module call) ──────────────────────
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
.info-box {
    background: #fff8e1;
    border-left: 4px solid #f9a825;
    border-radius: 0 8px 8px 0;
    padding: .9rem 1.2rem;
    margin-bottom: 1rem;
    color: #5d4e12;
    font-size: .92rem;
    line-height: 1.6;
}
</style>
"""

# ─── Rumus / penjelasan singkat per satuan ──────────────────────────────────
INFO = {
    "Normalitas (N)": "N = jumlah ekuivalen zat terlarut per liter larutan. N = M × valensi",
    "Molaritas (M)": "M = mol zat terlarut per liter larutan. M = (massa/Mr) / V(L)",
    "Molalitas (m)": "m = mol zat terlarut per kg pelarut. m = (massa/Mr) / kg_pelarut",
    "%b/v": "% b/v = (massa zat terlarut (g) / volume larutan (mL)) × 100",
    "%b/b": "% b/b = (massa zat terlarut (g) / massa larutan (g)) × 100",
    "ppm (mg/L)": "ppm = mg zat per liter larutan (≈ mg/kg untuk larutan encer)",
    "ppb (µg/L)": "ppb = µg zat per liter larutan",
}

SATUAN_LIST = list(INFO.keys())


# ─── Fungsi konversi ─────────────────────────────────────────────────────────
# Strategi: konversi semua ke "mol/L" (Molaritas) sebagai satuan pivot,
# kemudian dari pivot ke satuan tujuan.
# Beberapa konversi butuh parameter tambahan (Mr, valensi, densitas, dll.).

def ke_molaritas(nilai, satuan_asal, **kw):
    """Konversi nilai dari satuan_asal → Molaritas (mol/L). Kembalikan float atau raise."""
    mr = kw.get("mr", 1.0)          # Massa molar (g/mol)
    valensi = kw.get("valensi", 1)  # Valensi ion
    rho = kw.get("rho", 1.0)        # Densitas larutan (g/mL) — default air
    kg_pelarut = kw.get("kg_pelarut", 1.0)  # kg pelarut (untuk molalitas)

    if satuan_asal == "Normalitas (N)":
        return nilai / valensi
    elif satuan_asal == "Molaritas (M)":
        return nilai
    elif satuan_asal == "Molalitas (m)":
        # m = mol/kg_pelarut; butuh densitas utk ubah ke M (approx untuk larutan encer)
        # M ≈ (m * rho * 1000) / (1000 + m * mr)  — rumus eksak
        return (nilai * rho * 1000) / (1000 + nilai * mr)
    elif satuan_asal == "%b/v":
        # % b/v = g/100mL → g/L = nilai*10 → mol/L = (nilai*10)/mr
        return (nilai * 10) / mr
    elif satuan_asal == "%b/b":
        # % b/b: rho diperlukan
        # g zat per g larutan × rho(g/mL) × 1000 mL/L / mr
        return (nilai / 100) * rho * 1000 / mr
    elif satuan_asal == "ppm (mg/L)":
        # ppm = mg/L → mol/L = (mg/L) / (mr * 1000)
        return nilai / (mr * 1000)
    elif satuan_asal == "ppb (µg/L)":
        # ppb = µg/L → mol/L = (µg/L) / (mr * 1e6)
        return nilai / (mr * 1e6)
    else:
        raise ValueError(f"Satuan tidak dikenal: {satuan_asal}")


def dari_molaritas(molaritas, satuan_tujuan, **kw):
    """Konversi Molaritas → satuan_tujuan."""
    mr = kw.get("mr", 1.0)
    valensi = kw.get("valensi", 1)
    rho = kw.get("rho", 1.0)

    if satuan_tujuan == "Molaritas (M)":
        return molaritas
    elif satuan_tujuan == "Normalitas (N)":
        return molaritas * valensi
    elif satuan_tujuan == "Molalitas (m)":
        # m = M / (rho*1000 - M*mr) * 1000
        denom = rho * 1000 - molaritas * mr
        if denom <= 0:
            raise ValueError("Densitas terlalu kecil untuk konversi molalitas.")
        return (molaritas * 1000) / denom
    elif satuan_tujuan == "%b/v":
        return (molaritas * mr) / 10
    elif satuan_tujuan == "%b/b":
        return (molaritas * mr) / (rho * 10)
    elif satuan_tujuan == "ppm (mg/L)":
        return molaritas * mr * 1000
    elif satuan_tujuan == "ppb (µg/L)":
        return molaritas * mr * 1e6
    else:
        raise ValueError(f"Satuan tidak dikenal: {satuan_tujuan}")


def needs_valensi(s_asal, s_tujuan):
    return "Normalitas (N)" in (s_asal, s_tujuan)

def needs_rho(s_asal, s_tujuan):
    return any(x in (s_asal, s_tujuan) for x in ["%b/b", "Molalitas (m)"])

def needs_mr(s_asal, s_tujuan):
    # Jika kedua satuan adalah mol-based (N, M, m) saja, mr tidak selalu wajib
    mol_only = {"Normalitas (N)", "Molaritas (M)", "Molalitas (m)"}
    return not ({s_asal, s_tujuan}.issubset(mol_only))


# ─── Halaman utama ───────────────────────────────────────────────────────────
def halaman_kimia():
    st.markdown(SHARED_CSS, unsafe_allow_html=True)
    st.markdown('<div class="hero-title" style="font-size:2.6rem">Konversi Kimia 🧪</div>', unsafe_allow_html=True)
    st.markdown("Konversi satuan konsentrasi larutan dengan mudah dan akurat.", unsafe_allow_html=False)
    st.markdown('<hr style="border:none;border-top:1.5px solid rgba(44,83,100,.1);margin:1rem 0">', unsafe_allow_html=True)

    col_input, col_result = st.columns([1, 1], gap="large")

    with col_input:
        st.markdown('<div class="section-header">⚙️ Parameter Konversi</div>', unsafe_allow_html=True)

        satuan_tujuan = st.selectbox("📌 Satuan Tujuan (yang ingin dicari)", SATUAN_LIST, key="chem_tujuan")

        asal_options = [s for s in SATUAN_LIST if s != satuan_tujuan]
        satuan_asal = st.selectbox("📐 Satuan Asal (yang kamu ketahui)", asal_options, key="chem_asal")

        nilai = st.number_input(
            f"Nilai dalam {satuan_asal}",
            min_value=0.0,
            format="%.6f",
            key="chem_nilai",
        )

        st.markdown("---")
        st.markdown("**Parameter Tambahan**")
        st.caption("Isi sesuai zat yang digunakan. Abaikan jika tidak relevan.")

        mr = 1.0
        valensi = 1
        rho = 1.0

        if needs_mr(satuan_asal, satuan_tujuan):
            mr = st.number_input("Massa Molar (Mr) zat [g/mol]", min_value=0.001, value=58.44,
                                  help="Contoh: NaCl = 58.44, H₂SO₄ = 98.08", key="chem_mr")

        if needs_valensi(satuan_asal, satuan_tujuan):
            valensi = st.number_input("Valensi / Faktor Ekuivalen", min_value=1, value=1,
                                       help="Jumlah H⁺ atau OH⁻ yang dilepaskan. HCl=1, H₂SO₄=2", key="chem_val")

        if needs_rho(satuan_asal, satuan_tujuan):
            rho = st.number_input("Densitas larutan [g/mL]", min_value=0.001, value=1.0,
                                   help="Densitas air = 1.0 g/mL", key="chem_rho")

        tombol = st.button("🔄 Konversi Sekarang", key="btn_kimia")

    with col_result:
        st.markdown('<div class="section-header">📊 Hasil Konversi</div>', unsafe_allow_html=True)

        # Info rumus
        st.markdown(
            f'<div class="info-box">ℹ️ <b>{satuan_tujuan}</b><br>{INFO[satuan_tujuan]}</div>',
            unsafe_allow_html=True,
        )

        if tombol:
            try:
                kw = {"mr": mr, "valensi": valensi, "rho": rho}
                mol_l = ke_molaritas(nilai, satuan_asal, **kw)
                hasil = dari_molaritas(mol_l, satuan_tujuan, **kw)

                # Label singkat untuk tampilan
                unit_labels = {
                    "Normalitas (N)": "N",
                    "Molaritas (M)": "M",
                    "Molalitas (m)": "m",
                    "%b/v": "% b/v",
                    "%b/b": "% b/b",
                    "ppm (mg/L)": "ppm",
                    "ppb (µg/L)": "ppb",
                }
                unit_short = unit_labels.get(satuan_tujuan, "")

                st.markdown(f"""
                <div class="result-box">
                    <div class="result-label">Hasil Konversi</div>
                    <div class="result-value">{hasil:,.6g} <span style="font-size:1.1rem;color:#4a9db5">{unit_short}</span></div>
                    <div style="margin-top:.5rem;font-size:.85rem;color:#4a7a90">
                        {nilai} {unit_labels.get(satuan_asal,'')} → {hasil:,.6g} {unit_short}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Detail via molaritas pivot
                st.markdown("---")
                st.markdown("##### 🧮 Detail Perhitungan")
                st.markdown(f"""
                | Langkah | Nilai |
                |---------|-------|
                | Nilai masukan | `{nilai} {unit_labels.get(satuan_asal,'')}` |
                | Konversi ke Molaritas (pivot) | `{mol_l:.6g} M` |
                | Konversi ke {satuan_tujuan} | `{hasil:.6g} {unit_short}` |
                | Mr digunakan | `{mr} g/mol` |
                | Valensi | `{int(valensi)}` |
                | Densitas | `{rho} g/mL` |
                """)

            except Exception as e:
                st.error(f"❌ Terjadi kesalahan: {e}")
        else:
            st.markdown("""
            <div style="text-align:center;padding:3rem 1rem;color:#8ab0be">
                <div style="font-size:3rem">⚗️</div>
                <div style="margin-top:.5rem;font-size:1rem">
                    Masukkan parameter di sebelah kiri<br>lalu klik <b>Konversi Sekarang</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Tabel referensi ──────────────────────────────────────────────────────
    with st.expander("📚 Referensi Rumus Konversi Konsentrasi"):
        st.markdown("""
| Satuan | Definisi | Rumus Utama |
|--------|----------|-------------|
| **Molaritas (M)** | mol zat / L larutan | M = n/V |
| **Normalitas (N)** | ekuivalen / L larutan | N = M × valensi |
| **Molalitas (m)** | mol zat / kg pelarut | m = n / kg_pelarut |
| **% b/v** | g zat / 100 mL larutan | % = (m_zat / V_lar) × 100 |
| **% b/b** | g zat / 100 g larutan | % = (m_zat / m_lar) × 100 |
| **ppm** | mg zat / L larutan | ppm = mg/L |
| **ppb** | µg zat / L larutan | ppb = µg/L |
        """)
