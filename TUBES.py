import pandas as pd
import numpy as np


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

    data_semua = []
    for nama_file, brand in daftar_file:
        try:
            data = pd.read_csv(nama_file)
            data["brand"] = brand
            data_semua.append(data)
        except FileNotFoundError:
            print(f"File {nama_file} tidak ditemukan, data dilewati.")

    if len(data_semua) == 0:
        raise FileNotFoundError("Tidak ada file dataset mobil yang ditemukan.")

    return pd.concat(data_semua, ignore_index=True)


dp_asli = load_data_mobil()


def trimf(x, a, b, c):
    if x <= a or x >= c:
        return 0
    elif x == b:
        return 1
    elif x < b:
        return (x - a) / (b - a)
    else:
        return (c - x) / (c - b)


def trapmf(x, a, b, c, d):
    if x <= a or x > d:
        return 0
    elif a < x <= b:
        return (x - a) / (b - a)
    elif b < x <= c:
        return 1
    else:
        return (d - x) / (d - c)


# Membership function output
def tidakRekomen(x):
    return trapmf(x, 0, 0, 30, 50)


def rekomen(x):
    return trimf(x, 40, 60, 80)


def sangatRekomen(x):
    return trapmf(x, 70, 85, 100, 100)


score = np.arange(0, 101, 1)

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
    # Sangat rekomendasi: mobil relatif baru, mileage rendah, irit, dan pajak rendah.
    rule1 = min(fuzzy["yBaru"], fuzzy["mRendah"])
    rule2 = min(fuzzy["yBaru"], fuzzy["mpgEfisien"])
    rule3 = min(fuzzy["yBaru"], fuzzy["tRendah"])
    rule4 = min(fuzzy["pMurah"], fuzzy["tRendah"])
    rule5 = min(fuzzy["yBaru"], fuzzy["mRendah"], fuzzy["tRendah"])
    rule6 = min(fuzzy["mRendah"], fuzzy["mpgEfisien"], fuzzy["tRendah"])
    rule7 = min(fuzzy["yBaru"], fuzzy["mSedang"], fuzzy["mpgEfisien"])
    rule8 = min(fuzzy["pMurah"], fuzzy["yBaru"])
    rule9 = min(fuzzy["pMurah"], fuzzy["mRendah"])
    rule10 = min(fuzzy["pMurah"], fuzzy["mpgEfisien"])

    # Rekomendasi: kondisi masih cukup bagus, tetapi tidak sekuat kategori atas.
    rule11 = min(fuzzy["ySedang"], fuzzy["mSedang"])
    rule12 = min(fuzzy["mSedang"], fuzzy["mpgSedang"])
    rule13 = min(fuzzy["pSedang"], fuzzy["tSedang"])
    rule14 = min(fuzzy["yBaru"], fuzzy["mSedang"])
    rule15 = min(fuzzy["mSedang"], fuzzy["mpgEfisien"])
    rule16 = min(fuzzy["pSedang"], fuzzy["ySedang"])
    rule17 = min(fuzzy["pSedang"], fuzzy["mSedang"])
    rule18 = min(fuzzy["pSedang"], fuzzy["mpgEfisien"])

    # Tidak rekomendasi: mobil tua, mileage tinggi, boros, mesin besar, atau pajaknya tinggi.
    rule19 = min(fuzzy["yTua"], fuzzy["mTinggi"])
    rule20 = min(fuzzy["yTua"], fuzzy["mSangatTinggi"])
    rule21 = min(fuzzy["mTinggi"], fuzzy["tTinggi"])
    rule22 = min(fuzzy["mTinggi"], fuzzy["mpgTidakEfisien"])
    rule23 = min(fuzzy["pMahal"], fuzzy["tTinggi"])
    rule24 = min(fuzzy["mSangatTinggi"], fuzzy["tTinggi"])
    rule25 = min(fuzzy["mpgTidakEfisien"], fuzzy["tTinggi"])
    rule26 = min(fuzzy["pMahal"], fuzzy["yTua"])
    rule27 = min(fuzzy["pMahal"], fuzzy["mTinggi"])
    rule28 = min(fuzzy["pMahal"], fuzzy["mpgTidakEfisien"])

    sangatRekomenRule = max(rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10)
    rekomenRule = max(rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18)
    tidakRekomenRule = max(rule19, rule20, rule21, rule22, rule23, rule24, rule25, rule26, rule27, rule28)

    return sangatRekomenRule, rekomenRule, tidakRekomenRule


def fuzzy_mamdani(year, mileage, mpg, price, tax):
    fuzzy = fuzzyfication(year, mileage, mpg, price, tax)
    sangatRekomenRule, rekomenRule, tidakRekomenRule = rule(fuzzy)

    sangatRekomenClip = np.array([min(sangatRekomenRule, sangatRekomen(x)) for x in score])
    rekomenClip = np.array([min(rekomenRule, rekomen(x)) for x in score])
    tidakRekomenClip = np.array([min(tidakRekomenRule, tidakRekomen(x)) for x in score])

    aggregated = np.maximum.reduce([
        sangatRekomenClip,
        rekomenClip,
        tidakRekomenClip,
    ])

    if np.sum(aggregated) == 0:
        return 0
    else:
        return np.sum(score * aggregated) / np.sum(aggregated)


def fuzzy_sugeno(year, mileage, mpg, price, tax):
    fuzzy = fuzzyfication(year, mileage, mpg, price, tax)
    sangatRekomenRule, rekomenRule, tidakRekomenRule = rule(fuzzy)

    penyebut = sangatRekomenRule + rekomenRule + tidakRekomenRule
    if penyebut == 0:
        return 0
    else:
        hasil = (sangatRekomenRule * 100 + rekomenRule * 70 + tidakRekomenRule * 25) / penyebut
        return hasil

def get_numeric_input(prompt, default, value_type=float):
    while True:
        raw = input(f"{prompt} (default = {default}): ").strip()
        if raw == "":
            return value_type(default)
        try:
            return value_type(raw)
        except ValueError:
            print("Input tidak valid, gunakan angka.")


def main():
    print("Sistem rekomendasi mobil berdasarkan kebutuhan pengguna")
    print("Silakan masukkan preferensi Anda. Tekan Enter untuk menggunakan nilai default.\n")

    min_year = get_numeric_input("Tahun minimum kendaraan", 2015, int)
    max_mileage = get_numeric_input("Mileage maksimum", 80000, int)
    min_mpg = get_numeric_input("MPG minimum", 40.0, float)
    max_price = get_numeric_input("Budget maksimum (£)", 20000, int)
    max_tax = get_numeric_input("Pajak maksimum", 150, int)

    kandidat = dp_asli[
        (dp_asli["year"] >= min_year)
        & (dp_asli["mileage"] <= max_mileage)
        & (dp_asli["mpg"] >= min_mpg)
        & (dp_asli["price"] <= max_price)
        & (dp_asli["tax"] <= max_tax)
    ]

    if len(kandidat) == 0:
        print("\nTidak ada mobil yang memenuhi kriteria Anda.")
    else:
        print(f"\nDitemukan {len(kandidat)} kandidat yang cocok. Menampilkan rekomendasi teratas.\n")
        
        hasil = []
        for _, row in kandidat.iterrows():
            brand = row["brand"]
            model = row["model"]
            year = row["year"]
            price = row["price"]
            transmission = row["transmission"]
            mileage = row["mileage"]
            fuel_type = row["fuelType"]
            tax = row["tax"]
            mpg = row["mpg"]
            engine_size = row["engineSize"]
        
            hasil_mamdani = fuzzy_mamdani(year, mileage, mpg, price, tax)
            hasil_sugeno = fuzzy_sugeno(year, mileage, mpg, price, tax)
            hasil_akhir = (hasil_mamdani + hasil_sugeno) / 2
        
            hasil.append([
                brand,
                model,
                year,
                price,
                transmission,
                mileage,
                fuel_type,
                tax,
                mpg,
                engine_size,
                hasil_mamdani,
                hasil_sugeno,
                hasil_akhir,
            ])
        
        kolom_hasil = [
            "brand",
            "model",
            "year",
            "price",
            "transmission",
            "mileage",
            "fuelType",
            "tax",
            "mpg",
            "engineSize",
            "Mamdani",
            "Sugeno",
            "Skor Akhir",
        ]
        
        dp_hasil = pd.DataFrame(hasil, columns=kolom_hasil)
        dp_hasil = dp_hasil.sort_values("Skor Akhir", ascending=False)
        
        print("Top 10 rekomendasi mobil sesuai kebutuhan Anda:")
        print(dp_hasil.head(10).round(2).to_string(index=False))


if __name__ == "__main__":
    main()
