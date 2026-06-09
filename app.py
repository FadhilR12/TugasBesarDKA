import streamlit as st
import pandas as pd
import numpy as np
import os
import base64

# ============================================================
# Page Configuration
# ============================================================
st.set_page_config(
    page_title="Rekomendasi Mobil Bekas Cerdas",
    layout="wide",
)

# ============================================================
# Paths
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")


# ============================================================
# Image handling — use Streamlit static file serving
# ============================================================
def get_image_base64(filename):
    """Return base64-encoded data URI for a small image."""
    filepath = os.path.join(ASSETS_DIR, filename)
    try:
        with open(filepath, "rb") as f:
            data = base64.b64encode(f.read()).decode()
        return f"data:image/png;base64,{data}"
    except FileNotFoundError:
        return ""


# Cache images so they're only read once
@st.cache_data
def load_car_images():
    return {
        "sedan": get_image_base64("car_sedan.png"),
        "luxury": get_image_base64("car_luxury.png"),
        "hatchback": get_image_base64("car_hatchback.png"),
        "suv": get_image_base64("car_suv.png"),
    }


CAR_IMAGES = load_car_images()

BRAND_IMG = {
    "BMW": "luxury",
    "Mercedes": "luxury",
    "Audi": "sedan",
    "Toyota": "suv",
    "Ford": "suv",
    "Hyundai": "hatchback",
    "Skoda": "hatchback",
    "Vauxhall": "hatchback",
    "Volkswagen": "sedan",
}


def car_img_src(brand):
    key = BRAND_IMG.get(brand, "sedan")
    return CAR_IMAGES.get(key, CAR_IMAGES.get("sedan", ""))

st.markdown("""
<style>
header {
    visibility: hidden;
}

[data-testid="stHeader"] {
    display: none;
}

[data-testid="stToolbar"] {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# CSS — Design System  (Light, 1920×1080 optimized)
# Primary #0F172A · Secondary #3B82F6 · Tertiary #10B981 · Neutral #64748B
# ============================================================
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

:root{
  --primary:#0F172A;--primary-light:#1E293B;
  --secondary:#3B82F6;--secondary-light:#60A5FA;
  --secondary-bg:rgba(59,130,246,.08);--secondary-border:rgba(59,130,246,.2);
  --tertiary:#10B981;--tertiary-light:#34D399;
  --tertiary-bg:rgba(16,185,129,.08);--tertiary-border:rgba(16,185,129,.2);
  --neutral:#64748B;--neutral-light:#94A3B8;
  --n100:#F1F5F9;--n200:#E2E8F0;--n300:#CBD5E1;
  --danger:#EF4444;--danger-bg:rgba(239,68,68,.08);--danger-border:rgba(239,68,68,.2);
  --white:#FFF;--bg:#F0F4F8;
  --shadow:0 1px 3px rgba(15,23,42,.06),0 1px 2px rgba(15,23,42,.04);
  --shadow-hover:0 10px 25px rgba(15,23,42,.08),0 4px 10px rgba(15,23,42,.04);
  --radius:16px;--radius-sm:10px;--radius-xs:8px;
  --ease:all .25s cubic-bezier(.4,0,.2,1);
}

/* --- global --- */
.stApp{background:var(--bg)!important;font-family:'Inter',sans-serif!important}
.stApp>header{background:transparent!important}
#MainMenu,footer,.stDeployButton{display:none!important}

/* --- wide layout for 1920 --- */
.block-container{max-width:1440px!important;padding:1rem 2rem!important}

/* --- navbar (full-width edge-to-edge) --- */
.navbar{background:var(--white);border-bottom:1px solid var(--n200);padding:.75rem 2.5rem;display:flex;align-items:center;justify-content:space-between;position:fixed;top:0;left:0;right:0;width:100vw;z-index:9999;box-sizing:border-box}
.navbar-spacer{height:60px}
.navbar-links{display:flex;gap:.35rem}
.navbar-link{width:36px;height:36px;border-radius:50%;border:1.5px solid var(--n200);display:flex;align-items:center;justify-content:center;color:var(--primary);font-size:1rem;background:transparent;cursor:pointer;transition:var(--ease)}
.navbar-link:hover{background:var(--n100);border-color:var(--n300)}
.navbar-link.active{background:var(--primary);color:var(--white);border-color:var(--primary)}

/* --- hero --- */
.hero{max-width:1000px;margin:1.5rem auto 2rem;text-align:justify;padding:0}
.hero h1{font-size:2.6rem;font-weight:900;color:var(--primary);letter-spacing:-.03em;line-height:1.15;margin-bottom:1rem}
.hero p{font-size:1.05rem;color:var(--neutral);line-height:1.7;max-width:640px}

/* --- stats --- */
.stats-strip{display:flex;gap:1rem;margin:1.5rem auto 2rem;max-width:1000px}
.stat-pill{flex:1;background:var(--white);border:1px solid var(--n200);border-radius:12px;padding:1rem 1.25rem;text-align:center;box-shadow:var(--shadow);transition:var(--ease)}
.stat-pill:hover{border-color:var(--secondary-border);box-shadow:var(--shadow-hover)}
.stat-pill-value{font-size:1.35rem;font-weight:800;color:var(--primary)}
.stat-pill-label{font-size:.65rem;font-weight:500;color:var(--neutral);text-transform:uppercase;letter-spacing:.06em;margin-top:.15rem}

/* --- section card --- */
.section-card{background:var(--white);border:1px solid var(--n200);border-radius:var(--radius);padding:1.25rem 1.5rem;margin-bottom:1.25rem;box-shadow:var(--shadow)}
.section-header{display:flex;align-items:center;gap:.6rem;margin-bottom:0}
.section-title{font-size:1rem;font-weight:700;color:var(--primary)}
.section-desc{font-size:.75rem;color:var(--neutral)}

/* --- filter badges --- */
.filter-bar{display:flex;align-items:center;gap:.5rem;flex-wrap:wrap;background:var(--white);border:1px solid var(--n200);border-radius:12px;padding:.75rem 1.25rem;margin:0 auto 1.5rem;max-width:1400px}
.filter-label{font-size:.8rem;font-weight:600;color:var(--neutral);white-space:nowrap;margin-right:.25rem}
.filter-badge{display:inline-flex;align-items:center;gap:.35rem;background:var(--secondary-bg);color:var(--secondary);border:1px solid var(--secondary-border);border-radius:100px;padding:.3rem .75rem;font-size:.75rem;font-weight:600;white-space:nowrap}
.filter-badge .x{opacity:.5;font-weight:400}

/* --- results summary --- */
.results-summary{display:flex;align-items:center;justify-content:space-between;max-width:1400px;margin:0 auto 1rem;padding:0}
.results-count{font-size:.9rem;font-weight:600;color:var(--primary)}
.results-count span{color:var(--secondary)}
.results-sort{font-size:.75rem;color:var(--neutral)}

/* --- cards grid (3 cols for 1920) --- */
.cards-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1.5rem;max-width:1400px;margin:0 auto 2rem}
@media(max-width:1200px){.cards-grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:700px){.cards-grid{grid-template-columns:1fr}}

/* --- car card --- */
.car-card{background:var(--white);border-radius:var(--radius);box-shadow:var(--shadow);overflow:hidden;transition:var(--ease);border:1px solid var(--n200);animation:cardIn .5s ease-out both}
.car-card:hover{box-shadow:var(--shadow-hover);transform:translateY(-4px)}
@keyframes cardIn{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}

.car-card-img-wrap{position:relative;overflow:hidden;background:linear-gradient(135deg,var(--n100),var(--n200));height:200px}
.car-card-img-wrap img{width:100%;height:200px;object-fit:cover;display:block}

/* badges */
.card-badge{position:absolute;top:12px;right:12px;display:inline-flex;align-items:center;gap:.3rem;padding:.3rem .7rem;border-radius:100px;font-size:.7rem;font-weight:600;backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px)}
.card-badge.sangat{background:rgba(16,185,129,.9);color:#fff}
.card-badge.layak{background:rgba(59,130,246,.9);color:#fff}
.card-badge.kurang{background:rgba(239,68,68,.85);color:#fff}
.card-badge-dot{width:6px;height:6px;border-radius:50%;background:#fff;display:inline-block}

.rank-badge{position:absolute;top:12px;left:12px;width:32px;height:32px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:.75rem;font-weight:800;color:#fff}
.rank-badge.r1{background:linear-gradient(135deg,#F59E0B,#D97706)}
.rank-badge.r2{background:linear-gradient(135deg,#94A3B8,#64748B)}
.rank-badge.r3{background:linear-gradient(135deg,#D97706,#92400E)}
.rank-badge.rn{background:var(--primary-light)}

.price-badge{position:absolute;bottom:12px;left:12px;background:rgba(15,23,42,.75);backdrop-filter:blur(8px);color:#fff;padding:.3rem .7rem;border-radius:8px;font-size:.8rem;font-weight:700}

/* card body */
.car-card-body{padding:1.25rem 1.25rem 1rem}
.car-card-top{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:.15rem}
.car-card-name{font-size:1.1rem;font-weight:700;color:var(--primary);line-height:1.3;flex:1;margin-right:.5rem}
.car-card-score{font-size:1.6rem;font-weight:800;line-height:1;text-align:right}
.car-card-score.high{color:var(--tertiary)}.car-card-score.medium{color:var(--secondary)}.car-card-score.low{color:var(--danger)}
.car-card-score-label{font-size:.6rem;font-weight:700;text-transform:uppercase;letter-spacing:.04em;margin-top:2px;text-align:right}
.car-card-score-label.high{color:var(--tertiary)}.car-card-score-label.medium{color:var(--secondary)}.car-card-score-label.low{color:var(--danger)}
.car-card-subtitle{font-size:.8rem;color:var(--neutral);margin-bottom:.75rem;font-weight:400}

/* specs */
.specs-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:.25rem;margin-bottom:.75rem;padding-top:.75rem;border-top:1px solid var(--n200)}
.spec-item{text-align:center;padding:.35rem 0}
.spec-label{font-size:.65rem;color:var(--neutral-light);font-weight:500;text-transform:uppercase;letter-spacing:.03em}
.spec-value{font-size:.82rem;font-weight:700;color:var(--primary);margin-top:2px}

/* gauge */
.gauge-container{padding-top:.5rem;border-top:1px solid var(--n200)}
.gauge-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:6px}
.gauge-label{font-size:.7rem;font-weight:600;color:var(--neutral)}
.gauge-value{font-size:.7rem;font-weight:700;color:var(--primary)}
.gauge-bar{width:100%;height:6px;background:var(--n200);border-radius:3px;overflow:hidden}
.gauge-fill{height:100%;border-radius:3px;transition:width 1.2s cubic-bezier(.4,0,.2,1)}
.gauge-fill.high{background:linear-gradient(90deg,var(--tertiary),var(--tertiary-light))}
.gauge-fill.medium{background:linear-gradient(90deg,var(--secondary),var(--secondary-light))}
.gauge-fill.low{background:linear-gradient(90deg,var(--danger),#F87171)}

/* --- form overrides --- */
.stSelectbox>div>div,.stNumberInput>div>div>input,.stTextInput>div>div>input{background-color:var(--white)!important;border:1.5px solid var(--n200)!important;border-radius:var(--radius-xs)!important;color:var(--primary)!important;font-family:'Inter',sans-serif!important;transition:var(--ease)!important}
.stSelectbox>div>div:focus-within,.stNumberInput>div>div>input:focus{border-color:var(--secondary)!important;box-shadow:0 0 0 3px rgba(59,130,246,.12)!important}
.stSelectbox label,.stNumberInput label,.stTextInput label,.stSlider label{color:var(--primary)!important;font-family:'Inter',sans-serif!important;font-weight:600!important;font-size:.8rem!important}

/* --- button --- */
.stButton>button{width:100%;background:var(--secondary)!important;color:#fff!important;border:none!important;border-radius:var(--radius-xs)!important;padding:.8rem 2rem!important;font-size:.95rem!important;font-weight:600!important;font-family:'Inter',sans-serif!important;transition:var(--ease)!important;box-shadow:0 2px 8px rgba(59,130,246,.25)!important}
.stButton>button:hover{background:#2563EB!important;transform:translateY(-1px)!important;box-shadow:0 4px 16px rgba(59,130,246,.35)!important}

/* --- misc --- */
.empty-state{text-align:center;padding:3rem 2rem;color:var(--neutral)}
.empty-state-icon{font-size:3rem;margin-bottom:.75rem}
.empty-state-title{font-size:1.1rem;font-weight:600;color:var(--primary);margin-bottom:.5rem}
.empty-state-desc{font-size:.85rem;color:var(--neutral);max-width:400px;margin:0 auto;line-height:1.6}
.info-section{max-width:1400px;margin:1rem auto 0}
.info-card{background:var(--white);border:1px solid var(--n200);border-radius:var(--radius);padding:1.5rem;box-shadow:var(--shadow)}
.info-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-top:1rem}
.info-item{padding:1rem;border-radius:var(--radius-sm);text-align:center}
.info-item.green{background:var(--tertiary-bg);border:1px solid var(--tertiary-border)}
.info-item.blue{background:var(--secondary-bg);border:1px solid var(--secondary-border)}
.info-item.red{background:var(--danger-bg);border:1px solid var(--danger-border)}
.info-item-label{font-size:.75rem;font-weight:700;margin-bottom:.25rem}
.info-item.green .info-item-label{color:var(--tertiary)}
.info-item.blue .info-item-label{color:var(--secondary)}
.info-item.red .info-item-label{color:var(--danger)}
.info-item-desc{font-size:.7rem;color:var(--neutral);line-height:1.5}
.app-footer{text-align:center;padding:2rem 1rem;color:var(--neutral-light);font-size:.75rem}
.stExpander{background:var(--white)!important;border:1px solid var(--n200)!important;border-radius:12px!important}
.stProgress>div>div>div{background:var(--secondary)!important}
</style>""", unsafe_allow_html=True)

# ============================================================
# Backend — Fuzzy Logic (synced exactly with TUBES.py)
# ============================================================
@st.cache_data
def load_data_mobil():
    daftar_file = [
        ("audi.csv", "Audi"),
        ("bmw.csv", "BMW"),
        ("ford.csv", "Ford"),
        ("hyundi.csv", "Hyundai"),
        ("merc.csv", "Mercedes"),
        ("skoda.csv", "Skoda"),
        ("toyota.csv", "Toyota"),
        ("vauxhall.csv", "Vauxhall"),
        ("vw.csv", "Volkswagen"),
    ]
    frames = []
    for fname, brand in daftar_file:
        try:
            df = pd.read_csv(os.path.join(BASE_DIR, fname))
            df["brand"] = brand
            frames.append(df)
        except FileNotFoundError:
            pass
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def trimf(x, a, b, c):
    if x <= a or x >= c:
        return 0.0
    elif x == b:
        return 1.0
    elif x < b:
        return (x - a) / (b - a)
    else:
        return (c - x) / (c - b)


def trapmf(x, a, b, c, d):
    if x <= a or x > d:
        return 0.0
    elif a < x <= b:
        return (x - a) / (b - a)
    elif b < x <= c:
        return 1.0
    else:
        return (d - x) / (d - c)


def tidakRekomen(x):
    return trapmf(x, 0, 0, 30, 50)

def rekomen(x):
    return trimf(x, 40, 60, 80)

def sangatRekomen(x):
    return trapmf(x, 70, 85, 100, 100)


score_arr = np.arange(0, 101, 1)


def fuzzyfication(year, mileage, mpg, price, tax):
    return {
        # YEAR
        "yTua": trapmf(year, 1997, 1997, 2006, 2012),
        "ySedang": trimf(year, 2010, 2014, 2016),
        "yBaru": trapmf(year, 2015, 2018, 2020, 2020),
        # MILEAGE
        "mRendah": trapmf(mileage, 0, 0, 30000, 50000),
        "mSedang": trimf(mileage, 40000, 60000, 90000),
        "mTinggi": trimf(mileage, 70000, 100000, 140000),
        "mSangatTinggi": trapmf(mileage, 120000, 140000, 250000, 250000),
        # MPG
        "mpgTidakEfisien": trapmf(mpg, 0, 0, 20, 35),
        "mpgSedang": trimf(mpg, 25, 40, 50),
        "mpgEfisien": trapmf(mpg, 45, 60, 150, 150),
        # PRICE
        "pMurah": trapmf(price, 0, 0, 15000, 30000),
        "pSedang": trimf(price, 20000, 40000, 60000),
        "pMahal": trapmf(price, 50000, 65000, 80000, 80000),
        # TAX
        "tRendah": trapmf(tax, 0, 0, 50, 80),
        "tSedang": trapmf(tax, 85, 100, 150, 200),
        "tTinggi": trapmf(tax, 180, 230, 500, 500),
    }


def rule(fuzzy):
    # Sangat rekomendasi (10 rules)
    r1  = min(fuzzy["yBaru"], fuzzy["mRendah"])
    r2  = min(fuzzy["yBaru"], fuzzy["mpgEfisien"])
    r3  = min(fuzzy["yBaru"], fuzzy["tRendah"])
    r4  = min(fuzzy["pMurah"], fuzzy["tRendah"])
    r5  = min(fuzzy["yBaru"], fuzzy["mRendah"], fuzzy["tRendah"])
    r6  = min(fuzzy["mRendah"], fuzzy["mpgEfisien"], fuzzy["tRendah"])
    r7  = min(fuzzy["yBaru"], fuzzy["mSedang"], fuzzy["mpgEfisien"])
    r8  = min(fuzzy["pMurah"], fuzzy["yBaru"])
    r9  = min(fuzzy["pMurah"], fuzzy["mRendah"])
    r10 = min(fuzzy["pMurah"], fuzzy["mpgEfisien"])

    # Rekomendasi (8 rules)
    r11 = min(fuzzy["ySedang"], fuzzy["mSedang"])
    r12 = min(fuzzy["mSedang"], fuzzy["mpgSedang"])
    r13 = min(fuzzy["pSedang"], fuzzy["tSedang"])
    r14 = min(fuzzy["yBaru"], fuzzy["mSedang"])
    r15 = min(fuzzy["mSedang"], fuzzy["mpgEfisien"])
    r16 = min(fuzzy["pSedang"], fuzzy["ySedang"])
    r17 = min(fuzzy["pSedang"], fuzzy["mSedang"])
    r18 = min(fuzzy["pSedang"], fuzzy["mpgEfisien"])

    # Tidak rekomendasi (10 rules)
    r19 = min(fuzzy["yTua"], fuzzy["mTinggi"])
    r20 = min(fuzzy["yTua"], fuzzy["mSangatTinggi"])
    r21 = min(fuzzy["mTinggi"], fuzzy["tTinggi"])
    r22 = min(fuzzy["mTinggi"], fuzzy["mpgTidakEfisien"])
    r23 = min(fuzzy["pMahal"], fuzzy["tTinggi"])
    r24 = min(fuzzy["mSangatTinggi"], fuzzy["tTinggi"])
    r25 = min(fuzzy["mpgTidakEfisien"], fuzzy["tTinggi"])
    r26 = min(fuzzy["pMahal"], fuzzy["yTua"])
    r27 = min(fuzzy["pMahal"], fuzzy["mTinggi"])
    r28 = min(fuzzy["pMahal"], fuzzy["mpgTidakEfisien"])

    sr = max(r1, r2, r3, r4, r5, r6, r7, r8, r9, r10)
    rr = max(r11, r12, r13, r14, r15, r16, r17, r18)
    tr = max(r19, r20, r21, r22, r23, r24, r25, r26, r27, r28)
    return sr, rr, tr


def fuzzy_mamdani(year, mileage, mpg, price, tax):
    fz = fuzzyfication(year, mileage, mpg, price, tax)
    sr, rr, tr = rule(fz)
    sr_c = np.array([min(sr, sangatRekomen(x)) for x in score_arr])
    rr_c = np.array([min(rr, rekomen(x)) for x in score_arr])
    tr_c = np.array([min(tr, tidakRekomen(x)) for x in score_arr])
    agg = np.maximum.reduce([sr_c, rr_c, tr_c])
    s = np.sum(agg)
    return np.sum(score_arr * agg) / s if s > 0 else 0.0


def fuzzy_sugeno(year, mileage, mpg, price, tax):
    fz = fuzzyfication(year, mileage, mpg, price, tax)
    sr, rr, tr = rule(fz)
    d = sr + rr + tr
    return (sr * 100 + rr * 70 + tr * 25) / d if d > 0 else 0.0


# ============================================================
# Helper functions
# ============================================================
def score_label(s):
    return "Sangat Layak" if s >= 70 else ("Layak" if s >= 50 else "Kurang Layak")

def score_cls(s):
    return "high" if s >= 70 else ("medium" if s >= 50 else "low")

def badge_cls(s):
    return "sangat" if s >= 70 else ("layak" if s >= 50 else "kurang")

def badge_text(s, m, sg):
    if s < 50:
        return "Low Match"
    return "Mamdani Optimized" if m >= sg else "Sugeno Optimized"

def depreciation(year):
    age = 2020 - year
    return "Low" if age <= 3 else ("Med" if age <= 7 else "High")


# ============================================================
# Load data
# ============================================================
dp = load_data_mobil()

# ============================================================
# UI — Navbar
# ============================================================
st.markdown("""
<div class="navbar">
    <div class="navbar-brand">
        <strong>Tugas Besar DKA</strong>
    </div>
    <div class="navbar-links">
        <div class="navbar-link active">🏠</div>
        <div class="navbar-link">🔍</div>
        <div class="navbar-link">👤</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# Hero
# ============================================================
st.markdown("""
<div class="hero">
    <h1>Rekomendasi Mobil Bekas Cerdas</h1>
    <p>
        Menggunakan algoritma <strong>Logika Fuzzy</strong> untuk mengevaluasi kelayakan
        kendaraan secara objektif. Sistem kami memproses data teknis mulai dari
        depresiasi tahun hingga efisiensi mesin untuk memberikan skor
        kepercayaan yang transparan bagi pengambilan keputusan Anda.
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# Data check
# ============================================================
if dp.empty:
    st.error("❌ Tidak ada file dataset yang ditemukan. Pastikan file CSV ada di folder yang sama.")
    st.stop()

brands = sorted(dp["brand"].unique().tolist())

# ============================================================
# Stats
# ============================================================
st.markdown(f"""
<div class="stats-strip">
    <div class="stat-pill">
        <div class="stat-pill-value">{len(dp):,}</div>
        <div class="stat-pill-label">Total Data</div>
    </div>
    <div class="stat-pill">
        <div class="stat-pill-value">{len(brands)}</div>
        <div class="stat-pill-label">Brand</div>
    </div>
    <div class="stat-pill">
        <div class="stat-pill-value">{int(dp['year'].min())}–{int(dp['year'].max())}</div>
        <div class="stat-pill-label">Tahun</div>
    </div>
    <div class="stat-pill">
        <div class="stat-pill-value">£{int(dp['price'].min()):,}–£{int(dp['price'].max()):,}</div>
        <div class="stat-pill-label">Harga</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# Filter Form
# ============================================================
st.markdown("""
<div class="section-card" style="max-width:1000px;margin:0 auto 1rem">
    <div class="section-header">
        <div>
            <div class="section-title">Preferensi Pencarian</div>
            <div class="section-desc">Atur kriteria untuk menemukan mobil terbaik</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

left, center, right = st.columns([1, 5, 1])

with center:
    with st.container(border=True, width="stretch"):
        min_year = st.number_input("Tahun Minimum", min_value=int(dp["year"].min()), max_value=int(dp["year"].max()), value=2015, step=1)
        max_mileage = st.number_input("Mileage Maks (mil)", min_value=0, max_value=int(dp["mileage"].max()), value=50000, step=5000, format="%d")
        min_mpg = st.number_input("MPG Minimum", min_value=0.0, max_value=float(dp["mpg"].max()), value=15.0, step=5.0, format="%.1f")
        max_price = st.number_input("Budget Maks (£)", min_value=0, max_value=int(dp["price"].max()), value=50000, step=1000)
        max_tax = st.number_input("Pajak Maks (£/thn)", min_value=0, max_value=int(dp["tax"].max()), value=150, step=10)
        top_n = st.number_input("Jumlah Rekomendasi", min_value=1, max_value=50, value=9, step=3)

        st.markdown("")
        go = st.button("Cari Rekomendasi", use_container_width=True)

# ============================================================
# Results
# ============================================================
if go:
    # Filter
    kand = dp[
        (dp["year"] >= min_year)
        & (dp["mileage"] <= max_mileage)
        & (dp["mpg"] >= min_mpg)
        & (dp["price"] <= max_price)
        & (dp["tax"] <= max_tax)
    ].copy()

    if kand.empty:
        st.markdown("""
        <div class="section-card" style="max-width:700px;margin:2rem auto">
            <div class="empty-state">
                <div class="empty-state-icon">🔍</div>
                <div class="empty-state-title">Tidak Ada Mobil yang Cocok</div>
                <div class="empty-state-desc">
                    Coba ubah kriteria pencarian Anda, misalnya turunkan tahun minimum
                    atau naikkan budget maksimum.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Calculate scores
        bar = st.progress(0, text="🧠 Menghitung skor fuzzy...")
        results = []
        total = len(kand)
        for idx, (_, row) in enumerate(kand.iterrows()):
            ms = fuzzy_mamdani(row["year"], row["mileage"], row["mpg"], row["price"], row["tax"])
            ss = fuzzy_sugeno(row["year"], row["mileage"], row["mpg"], row["price"], row["tax"])
            fs = (ms + ss) / 2.0
            results.append({
                "brand": row["brand"], "model": row["model"],
                "year": int(row["year"]), "price": int(row["price"]),
                "transmission": row["transmission"],
                "mileage": int(row["mileage"]), "fuelType": row["fuelType"],
                "tax": int(row["tax"]), "mpg": float(row["mpg"]),
                "engineSize": float(row["engineSize"]),
                "Mamdani": round(ms, 2), "Sugeno": round(ss, 2),
                "Skor Akhir": round(fs, 2),
            })
            bar.progress((idx + 1) / total)
        bar.empty()

        df_res = pd.DataFrame(results).sort_values("Skor Akhir", ascending=False).reset_index(drop=True)
        top_df = df_res.head(top_n)

        # Filter badges
        st.markdown(f"""
        <div class="filter-bar">
            <span class="filter-label">Filter Aktif:</span>
            <span class="filter-badge">Tahun: >{min_year} <span class="x">×</span></span>
            <span class="filter-badge">Mileage: <{max_mileage // 1000}k <span class="x">×</span></span>
            <span class="filter-badge">MPG: >{min_mpg:.0f} <span class="x">×</span></span>
            <span class="filter-badge">Budget: <£{max_price:,} <span class="x">×</span></span>
            <span class="filter-badge">Tax: <£{max_tax} <span class="x">×</span></span>
        </div>
        """, unsafe_allow_html=True)

        # Summary
        st.markdown(f"""
        <div class="results-summary">
            <div class="results-count">
                Ditemukan <span>{len(kand)}</span> mobil — menampilkan Top <span>{len(top_df)}</span>
            </div>
            <div class="results-sort">Diurutkan berdasarkan skor tertinggi</div>
        </div>
        """, unsafe_allow_html=True)

        # Render cards using st.columns (3 per row) — avoids base64 image size limit
        rows_data = list(top_df.iterrows())
        for row_start in range(0, len(rows_data), 3):
            chunk = rows_data[row_start : row_start + 3]
            cols = st.columns(3)
            for col_idx, (df_idx, row) in enumerate(chunk):
                rank = row_start + col_idx + 1
                sk = row["Skor Akhir"]
                cls = score_cls(sk)
                bcls = badge_cls(sk)
                lab = score_label(sk)
                btxt = badge_text(sk, row["Mamdani"], row["Sugeno"])
                dep = depreciation(row["year"])
                img = car_img_src(row["brand"])

                rcls = {1: "r1", 2: "r2", 3: "r3"}.get(rank, "rn")
                delay = min(rank * 0.06, 0.6)

                with cols[col_idx]:
                    st.markdown(f"""
                    <div class="car-card" style="animation-delay:{delay}s">
                        <div class="car-card-img-wrap">
                            <img src="{img}" alt="{row['brand']} {row['model']}"/>
                            <div class="rank-badge {rcls}">#{rank}</div>
                            <div class="card-badge {bcls}">
                                <span class="card-badge-dot"></span>{btxt}
                            </div>
                            <div class="price-badge">£{row['price']:,}</div>
                        </div>
                        <div class="car-card-body">
                            <div class="car-card-top">
                                <div>
                                    <div class="car-card-name">{row['brand']} {row['model']}</div>
                                    <div class="car-card-subtitle">{row['engineSize']}L {row['transmission']} · {row['year']}</div>
                                </div>
                                <div>
                                    <div class="car-card-score {cls}">{sk:.0f}%</div>
                                    <div class="car-card-score-label {cls}">{lab}</div>
                                </div>
                            </div>
                            <div class="specs-grid">
                                <div class="spec-item">
                                    <div class="spec-label">Mileage</div>
                                    <div class="spec-value">{row['mileage']:,} mi</div>
                                </div>
                                <div class="spec-item">
                                    <div class="spec-label">Konsumsi</div>
                                    <div class="spec-value">{row['mpg']:.1f} mpg</div>
                                </div>
                                <div class="spec-item">
                                    <div class="spec-label">Depresiasi</div>
                                    <div class="spec-value">{dep}</div>
                                </div>
                            </div>
                            <div class="gauge-container">
                                <div class="gauge-header">
                                    <span class="gauge-label">Confidence Gauge</span>
                                    <span class="gauge-value">{sk:.0f}/100</span>
                                </div>
                                <div class="gauge-bar">
                                    <div class="gauge-fill {cls}" style="width:{sk}%"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        # Data table
        with st.expander(f"📋 Lihat Tabel Data Lengkap (Top {len(top_df)})"):
            st.dataframe(
                top_df[[
                    "brand", "model", "year", "price", "transmission",
                    "mileage", "fuelType", "tax", "mpg", "engineSize",
                    "Mamdani", "Sugeno", "Skor Akhir",
                ]],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "brand": "Brand", "model": "Model",
                    "year": st.column_config.NumberColumn("Tahun", format="%d"),
                    "price": st.column_config.NumberColumn("Harga (£)", format="£%d"),
                    "transmission": "Transmisi",
                    "mileage": st.column_config.NumberColumn("Mileage", format="%d mi"),
                    "fuelType": "BBM",
                    "tax": st.column_config.NumberColumn("Pajak", format="£%d"),
                    "mpg": st.column_config.NumberColumn("MPG", format="%.1f"),
                    "engineSize": st.column_config.NumberColumn("Mesin", format="%.1fL"),
                    "Mamdani": st.column_config.ProgressColumn("Mamdani", min_value=0, max_value=100, format="%.1f"),
                    "Sugeno": st.column_config.ProgressColumn("Sugeno", min_value=0, max_value=100, format="%.1f"),
                    "Skor Akhir": st.column_config.ProgressColumn("Skor Akhir", min_value=0, max_value=100, format="%.1f"),
                },
            )

        # Info section
        st.markdown("""
        <div class="info-section">
            <div class="info-card">
                <div class="section-header" style="margin-bottom:.75rem">
                    <div>
                        <div class="section-title">Tentang Sistem Fuzzy Logic</div>
                        <div class="section-desc">Bagaimana sistem menghitung skor rekomendasi</div>
                    </div>
                </div>
                <div style="font-size:.85rem;color:#64748B;line-height:1.7;margin-bottom:.75rem">
                    Sistem menggunakan 5 variabel input (<strong>Tahun, Mileage, MPG, Harga, Pajak</strong>)
                    yang diproses melalui 28 aturan fuzzy. Skor akhir adalah rata-rata dari metode
                    <strong>Mamdani</strong> (centroid defuzzification) dan <strong>Sugeno</strong> (weighted average).
                </div>
                <div class="info-grid">
                    <div class="info-item green">
                        <div class="info-item-label">✅ Sangat Layak (≥70)</div>
                        <div class="info-item-desc">Mobil baru, mileage rendah, irit BBM, harga terjangkau, pajak rendah</div>
                    </div>
                    <div class="info-item blue">
                        <div class="info-item-label">👍 Layak (50–69)</div>
                        <div class="info-item-desc">Kondisi cukup baik dengan beberapa trade-off yang masih bisa diterima</div>
                    </div>
                    <div class="info-item red">
                        <div class="info-item-label">⚠️ Kurang Layak (&lt;50)</div>
                        <div class="info-item-desc">Mobil tua, mileage tinggi, boros BBM, harga mahal, atau pajak tinggi</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# Footer
# ============================================================
st.markdown("""
<div class="app-footer">
    <p>Sistem Rekomendasi Mobil Bekas Cerdas</p>
    <p style="margin-top:.25rem">Fuzzy Logic (Mamdani &amp; Sugeno) · Tugas Besar DKA Semester 4</p>
</div>
""", unsafe_allow_html=True)
