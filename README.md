\
# SIM Laundry

Sistem Informasi Manajemen Operasional Jasa Laundry adalah aplikasi desktop Python untuk membantu pengelolaan pelanggan, paket layanan, transaksi laundry, serta pemantauan status cucian.

## Fitur utama

- Login pengguna.
- Registrasi pelanggan.
- Dashboard ringkasan operasional.
- Pengelolaan transaksi laundry.
- Tampilan sesuai peran pengguna yang diterapkan pada aplikasi.

## Struktur direktori

```text
Projek_UTS_PraktikumRPL_Klp3/
├── assets/                 # Logo dan aset tampilan
├── config/
│   └── database.py         # Konfigurasi koneksi MySQL
├── controller/
│   ├── auth_controller.py
│   └── laundry_controller.py
├── database/
│   ├── db_laundry.sql
│   └── users_table.sql
├── models/
│   ├── pelanggan_model.py
│   ├── paket_model.py
│   ├── transaksi_model.py
│   └── user_model.py
├── tests/
│   └── test_auth.py
├── views/
│   ├── customer_view.py
│   ├── dashboard_view.py
│   ├── laundry_view.py
│   ├── login_view.py
│   ├── manager_view.py
│   ├── register_view.py
│   └── splash_view.py
├── .github/workflows/
│   └── ci_pipeline.yml
├── main.py
├── pytest.ini
└── requirements.txt
```

## Persyaratan

- Windows 10/11
- Python 3.11 atau versi yang kompatibel dengan dependensi proyek
- Laragon dengan MySQL aktif
- Git (untuk mengirim perubahan ke GitHub)

## Instalasi dan konfigurasi database MySQL

1. Jalankan Laragon dan klik **Start All**.
2. Buka phpMyAdmin.
3. Pastikan database proyek tersedia. Pada konfigurasi awal proyek ini, nama database adalah `db_laundry_uas`.
4. Pastikan tabel `pelanggan`, `paket_layanan`, `transaksi_laundry`, dan `users` sudah tersedia.
5. Jika tabel akun belum dibuat, tinjau dan jalankan skrip `database/users_table.sql` pada database proyek sesuai struktur database yang digunakan.

Konfigurasi koneksi dapat diatur melalui environment variable berikut:

| Variabel              | Default          | Keterangan     |
|-----------------------|------------------|----------------|
| `LAUNDRY_DB_HOST`     | `localhost`      | Host MySQL     |
| `LAUNDRY_DB_NAME`     | `db_laundry`     | Nama database  |
| `LAUNDRY_DB_USER`     | `root`           | Username MySQL |
| `LAUNDRY_DB_PASSWORD` | kosong           | Password MySQL |
| `LAUNDRY_DB_PORT`     | `3306`           | Port MySQL     |

Jika nama database atau kredensial Laragon berbeda, atur environment variable tersebut sebelum menjalankan aplikasi.

## Menjalankan aplikasi dari source code

Buka terminal pada root proyek, lalu jalankan:

```powershell
python -m venv env
.\env\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python main.py
```

Pastikan MySQL Laragon aktif sebelum aplikasi dijalankan.

## Menjalankan unit test

Aktifkan virtual environment, kemudian jalankan:

```bash
python -m pytest -v
```

Konfigurasi `pytest.ini` membatasi discovery pengujian ke folder `tests/`. Skrip pemeriksaan manual lama di root proyek tidak dijalankan sebagai unit test otomatis.

## Continuous Integration dengan GitHub Actions

Workflow berada pada:

```text
.github/workflows/ci_pipeline.yml
```

Workflow berjalan ketika ada `push` atau `pull_request` ke branch `main`. Tahapannya:

1. Mengambil kode dari repository.
2. Menyiapkan Python 3.11.
3. Menginstal dependensi dari `requirements.txt`.
4. Menjalankan pemeriksaan Flake8 untuk kesalahan kritis pada folder `models/` dan `controller/`.
5. Menjalankan unit test dengan pytest.

Lihat hasilnya pada tab **Actions** di repository GitHub. Status hijau menunjukkan job berhasil.

## Packaging aplikasi Windows dengan PyInstaller

Jalankan perintah berikut dari root proyek pada Windows:

```powershell
pyinstaller --noconfirm --onefile --windowed --name "SIM_Laundry" --icon "assets/logo.ico" --add-data "assets;assets" main.py
```

Hasil executable akan dibuat di:

```text
dist/SIM_Laundry.exe
```

Uji file `.exe` pada komputer Windows. Pastikan MySQL Laragon aktif dan database dapat diakses. Jika aplikasi menggunakan database lokal, database tetap perlu disiapkan pada komputer tempat aplikasi dijalankan.

## GitHub Release

Setelah executable berhasil diuji:

1. Buka repository GitHub.
2. Pilih **Releases** lalu **Draft a new release**.
3. Buat tag `v1.0.0`.
4. Isi judul release, misalnya `SIM Laundry v1.0.0`.
5. Unggah `dist/SIM_Laundry.exe`.
6. Publikasikan release dan simpan screenshot sebagai bukti Modul VIII.

## Catatan

File executable dibuat untuk Windows. File database MySQL tidak otomatis menjadi bagian dari executable; layanan MySQL dan database harus tersedia dan dikonfigurasi pada komputer tempat aplikasi dijalankan.
