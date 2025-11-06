# Scan Image

## Langkah-langkah awal

### 1. Install Python 3.10

1. Unduh Python 3.10 dari situs web resmi:

   - Kunjungi [Python Downloads](https://www.python.org/downloads/release/python-3100/)
   - Unduh penginstal untuk sistem operasi (Windows, macOS, atau Linux)

2. Jalankan Penginstal:

   - Untuk Windows: Jalankan berkas .exe yang telah diunduh
   - Centang "Tambahkan Python 3.10 ke PATH" selama instalasi
   - Klik "Instal Sekarang"

3. Verifikasi instalasi:
   Buka Command Prompt (Windows) atau Terminal (macOS/Linux) dan jalankan:
   ```bash
   python --version
   ```
   Versi yang digunakan: `Python 3.10.x`

### 2. Clone Repository

```bash
git clone https://github.com/achmadzaenni/scan_image.git
cd scan_image
```

### 3. Install Required Libraries

Instal semua dependensi yang diperlukan menggunakan pip:

```bash
pip install -r requirements.txt
```

Ini akan menginstal semua pustaka yang diperlukan, termasuk:

- Flask
- OpenCV
- PaddleOCR
- PaddlePaddle
- Dll

## Running the Application

1. Pastikan Anda berada di direktori proyek:

   ```bash
   cd scan_image
   ```

2. Run Web:

   ```bash
   python app.py
   ```

3. Open Web:
   ```
   https://localhost:2025
   ```
   Note: Aplikasi ini menggunakan HTTPS dengan sertifikat yang ditandatangani sendiri (cert.pem dan key.pem)

## Penggunaan

1. Akses web dengan `https://localhost:2025`
2. Drag & Drop Image atau pilih image (format yang didukung: PNG, JPG, JPEG)
3. Maximum file size is 1MB
4. Klik "Upload" untuk memproses gambar
5. Teks yang diekstrak akan ditampilkan dan dapat disalin dari area teks

## Troubleshooting

1. Jika  mendapatkan kesalahan SSL/HTTPS:

   - Aplikasi menggunakan sertifikat yang ditandatangani sendiri
   -  mungkin perlu menerima risiko keamanan di peramban

2. Jika pustaka gagal diinstal:

   - Pastikan memiliki Python 3.10
   - Coba tingkatkan pip:
   ```bash
   python -m pip install --upgrade pip
   ```
   - Kemudian coba lagi menginstal persyaratan:
   ```bash
   pip install -r requirements.txt
   ```

3. Jika aplikasi tidak dapat dijalankan:
- Periksa apakah port 2025 tersedia di file app.py bawah sendiri
- Pastikan semua dependensi telah diinstal dengan benar
- Pastikan versi Python adalah 3.10
## HTTPS Setup

### Windows
1. Buat sertifikat:
   ```bash
   openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
   ```
   Note: Jika ssl belum terpasang unduh dari [OpenSSL for Windows](https://slproweb.com/products/Win32OpenSSL.html)

### macOS
1. Buat sertifikat bawaan openssl:
   ```bash
   openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
   ```

### Linux
1. Install OpenSSL jika belum terpasang:
   ```bash
   sudo apt-get install openssl
   sudo yum install openssl
   ```
2. Buat Sertifikat:
   ```bash
   openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
   ```

Setelah membuat sertifikat:
1. Pindahkan kedua file ssl (`cert.pem` dan `key.pem`) ke folder `scan_image`
2. Pastikan file sertifikat berada di folder yang sama dengan file `app.py`
3. File sertifikat harus bernama persis `cert.pem` dan `key.pem`