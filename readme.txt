# Sistem Fuzzy Logic Pemilihan 5 Restoran Terbaik

## Deskripsi Program
Program ini digunakan untuk memilih 5 restoran terbaik di Kota Bandung berdasarkan atribut:
- Kualitas Servis (1-100, semakin tinggi semakin baik)
- Harga (Rp25.000 - Rp55.000, semakin tinggi semakin mahal)

Proses pengambilan keputusan dilakukan menggunakan metode Fuzzy Logic, melalui tahapan:
- Fuzzifikasi
- Inferensi berbasis aturan
- Defuzzifikasi metode Centroid
- Menyimpan output ke file Excel

## Cara Menjalankan Program

1. Pastikan Anda sudah memiliki Python 3.x dan library `pandas` serta `openpyxl`.
   Jika belum, install dengan perintah:

2. Siapkan file `restoran.xlsx` berisi data restoran yang memiliki kolom:
- Pelayanan
- Harga

3. Jalankan program di terminal / command prompt:

4. Program akan:
- Membaca data dari `restoran.xlsx`
- Melakukan perhitungan Fuzzy
- Menampilkan 5 restoran terbaik di terminal
- Menyimpan hasil 5 restoran terbaik ke file `peringkat.xlsx`

## Struktur Output (peringkat.xlsx)
- ID Restoran
- Kualitas Servis
- Harga
- Skor Kelayakan

## Catatan
- Program ini tidak menggunakan library fuzzy system pihak ketiga.
- Seluruh proses fuzzy (fuzzifikasi, inferensi, defuzzifikasi) dibangun manual.
- Program secara otomatis mendeteksi nama kolom pelayanan dan harga berdasarkan nama kolom file Excel.
