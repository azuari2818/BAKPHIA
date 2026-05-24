# ⚗️ BAKPHIA — Bantuan Konversi Fisika & Kimia

[![CI](https://github.com/YOUR_USERNAME/bakphia/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/bakphia/actions)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://bakphia.streamlit.app)

Website konversi satuan Fisika dan Kimia berbasis Streamlit yang interaktif, akurat, dan mudah digunakan.

---

## 🚀 Fitur Utama

### 🧪 Konversi Kimia
Konversi antar satuan konsentrasi larutan:
- **Normalitas (N)**
- **Molaritas (M)**
- **Molalitas (m)**
- **%b/v** (gram per 100 mL)
- **%b/b** (gram per 100 gram)
- **ppm** (mg/L)
- **ppb** (µg/L)

> Mendukung parameter tambahan: Massa Molar (Mr), Valensi, dan Densitas larutan.

### ⚛️ Konversi Fisika
| Besaran | Satuan yang Didukung |
|---------|----------------------|
| 📏 Panjang | km, hm, dam, m, dm, cm, mm, µm, nm |
| ⚖️ Massa | kg, hg, dag, g, dg, cg, mg, µg, ng |
| 🌡️ Suhu | Celsius, Fahrenheit, Kelvin, Réaumur |
| ⚡ Energi | J, kJ, kal, kkal, kWh, eV, Erg |
| 💨 Tekanan | Pa, kPa, bar, atm, mmHg, cmHg, PSI, mbar |

### 🏠 Beranda
- Tujuan & Manfaat aplikasi
- **Jokes Kimia** acak yang berganti setiap kunjungan

---

## 🛠️ Instalasi & Menjalankan Lokal

```bash
# 1. Clone repo
git clone https://github.com/YOUR_USERNAME/bakphia.git
cd bakphia

# 2. (Opsional) buat virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install dependensi
pip install -r requirements.txt

# 4. Jalankan
streamlit run app.py
```

Buka browser di `http://localhost:8501`

---

## ☁️ Deploy ke Streamlit Community Cloud

1. Fork/push repo ini ke GitHub
2. Masuk ke [share.streamlit.io](https://share.streamlit.io)
3. Klik **New app** → pilih repo ini
4. **Main file path**: `app.py`
5. Klik **Deploy!**

---

## 📁 Struktur Project

```
bakphia/
├── app.py               # Entry point utama + halaman Beranda
├── konversi_kimia.py    # Modul konversi satuan konsentrasi
├── konversi_fisika.py   # Modul konversi besaran fisika
├── requirements.txt     # Dependensi Python
├── .github/
│   └── workflows/
│       └── ci.yml       # GitHub Actions CI
└── README.md
```

---

## 📐 Metode Konversi Kimia

Konversi kimia menggunakan **Molaritas sebagai satuan pivot**:

```
Satuan Asal → Molaritas (M) → Satuan Tujuan
```

| Konversi | Rumus |
|----------|-------|
| N → M | M = N / valensi |
| %b/v → M | M = (%b/v × 10) / Mr |
| %b/b → M | M = (%b/b × ρ × 10) / Mr |
| ppm → M | M = ppm / (Mr × 1000) |
| ppb → M | M = ppb / (Mr × 10⁶) |
| m → M | M = (m × ρ × 1000) / (1000 + m × Mr) |

---

## 📄 Lisensi

MIT License — bebas digunakan dan dimodifikasi.

---

*Dibuat dengan ❤️ menggunakan [Streamlit](https://streamlit.io)*
