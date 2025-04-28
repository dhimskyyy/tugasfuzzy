# Import library pandas untuk membaca dan menyimpan file Excel
import pandas as pd

# Fungsi untuk membaca data restoran dari file Excel
def baca_data(file_path):
    data = pd.read_excel(file_path)
    return data

# Fungsi untuk menghitung nilai fungsi keanggotaan segitiga
def segitiga(x, a, b, c):
    if x <= a or x >= c:
        return 0
    elif a < x < b:
        return (x - a) / (b - a)
    elif b <= x < c:
        return (c - x) / (c - b)
    else:
        return 0

# Fuzzifikasi untuk atribut Pelayanan
def fuzzifikasi_pelayanan(x):
    return {
        'Buruk': segitiga(x, 1, 1, 50),
        'Sedang': segitiga(x, 30, 50, 70),
        'Baik': segitiga(x, 60, 100, 100)
    }

# Fuzzifikasi untuk atribut Harga
def fuzzifikasi_harga(x):
    return {
        'Murah': segitiga(x, 25000, 25000, 40000),
        'Sedang': segitiga(x, 35000, 40000, 45000),
        'Mahal': segitiga(x, 40000, 55000, 55000)
    }

# Skor output defuzzifikasi berdasarkan kategori inferensi
output_score = {
    'Sangat Rendah': 12.5,
    'Rendah': 30,
    'Sedang': 50,
    'Tinggi': 70,
    'Sangat Tinggi': 87.5
}

# Aturan inferensi berbasis kombinasi Pelayanan dan Harga
aturan = {
    ('Buruk', 'Murah'): 'Rendah',
    ('Buruk', 'Sedang'): 'Rendah',
    ('Buruk', 'Mahal'): 'Sangat Rendah',
    ('Sedang', 'Murah'): 'Sedang',
    ('Sedang', 'Sedang'): 'Sedang',
    ('Sedang', 'Mahal'): 'Rendah',
    ('Baik', 'Murah'): 'Sangat Tinggi',
    ('Baik', 'Sedang'): 'Tinggi',
    ('Baik', 'Mahal'): 'Sedang'
}

# Fungsi inferensi untuk menentukan hasil berdasarkan fuzzifikasi
def inferensi(pelayanan_fuzz, harga_fuzz):
    hasil = []
    for s_kat, s_nilai in pelayanan_fuzz.items():
        for h_kat, h_nilai in harga_fuzz.items():
            min_nilai = min(s_nilai, h_nilai)
            if min_nilai > 0:
                kategori_output = aturan[(s_kat, h_kat)]
                hasil.append((min_nilai, kategori_output))
    return hasil

# Fungsi defuzzifikasi untuk menghitung skor akhir dari hasil inferensi
def defuzzifikasi(hasil_inferensi):
    if not hasil_inferensi:
        return 0
    pembilang = sum(nilai * output_score[kat] for nilai, kat in hasil_inferensi)
    penyebut = sum(nilai for nilai, _ in hasil_inferensi)
    return pembilang / penyebut if penyebut != 0 else 0

# Fungsi utama sistem fuzzy
def fuzzy_sistem(file_input, file_output):
    # Membaca data dari file input
    data = baca_data(file_input)
    print("Kolom dalam file:", list(data.columns))

    # Mendeteksi kolom pelayanan dan harga secara otomatis
    kolom_pelayanan = None
    kolom_harga = None
    for col in data.columns:
        if 'pelayanan' in col.lower():
            kolom_pelayanan = col
        if 'harga' in col.lower():
            kolom_harga = col

    # Validasi keberadaan kolom
    if kolom_pelayanan is None or kolom_harga is None:
        raise Exception("Tidak menemukan kolom 'Pelayanan' atau 'Harga'!")

    hasil = []
    # Proses untuk setiap data restoran
    for idx, row in data.iterrows():
        pelayanan = row[kolom_pelayanan]
        harga = row[kolom_harga]

        # Proses fuzzifikasi
        pelayanan_fuzz = fuzzifikasi_pelayanan(pelayanan)
        harga_fuzz = fuzzifikasi_harga(harga)

        # Proses inferensi
        hasil_inferensi = inferensi(pelayanan_fuzz, harga_fuzz)

        # Proses defuzzifikasi
        skor = defuzzifikasi(hasil_inferensi)

        # Menyimpan hasil dalam list
        hasil.append({
            'ID Restoran': idx + 1,
            kolom_pelayanan: pelayanan,
            kolom_harga: harga,
            'Skor Kelayakan': skor
        })

    # Mengurutkan hasil berdasarkan skor kelayakan (dari besar ke kecil)
    hasil = sorted(hasil, key=lambda x: x['Skor Kelayakan'], reverse=True)

    # Mengambil 5 restoran terbaik
    hasil_top5 = hasil[:5]

    # Menyimpan hasil ke file Excel output
    df_output = pd.DataFrame(hasil_top5)
    df_output.to_excel(file_output, index=False)

    # Menampilkan hasil di terminal
    print("\n5 Restoran Terbaik:")
    print(df_output)

# Program utama
if __name__ == "__main__":
    fuzzy_sistem('restoran.xlsx', 'peringkat.xlsx')
