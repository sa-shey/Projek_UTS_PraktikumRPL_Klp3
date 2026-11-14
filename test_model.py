
from models.pelanggan_model import PelangganModel
from models.paket_model import PaketModel

# Membuat objek model
pelanggan = PelangganModel()
paket = PaketModel()

print("\n=== TEST MODEL PELANGGAN ===")

# READ
print("Data pelanggan:")
print(pelanggan.tampilkan_pelanggan())

# CREATE
print("\nTambah pelanggan:")
hasil = pelanggan.tambah_pelanggan(
    9999,
    "Pelanggan Uji",
    "Jl. Percobaan",
    "081234567890"
)
print("Berhasil" if hasil else "Gagal")

# UPDATE
print("\nUpdate pelanggan:")
hasil = pelanggan.update_pelanggan(
    9999,
    "Pelanggan Uji Baru",
    "Jl. Percobaan Baru",
    "081234567891"
)
print("Berhasil" if hasil else "Gagal")

# DELETE
print("\nHapus pelanggan:")
hasil = pelanggan.hapus_pelanggan(9999)
print("Berhasil" if hasil else "Gagal")


print("\n=== TEST MODEL PAKET ===")

# READ
print("Data paket:")
print(paket.tampilkan_paket())

# CREATE
print("\nTambah paket:")
hasil = paket.tambah_paket(
    9999,
    "Paket Uji",
    "Reguler",
    7000
)
print("Berhasil" if hasil else "Gagal")

# UPDATE
print("\nUpdate paket:")
hasil = paket.update_paket(
    9999,
    "Paket Uji Baru",
    "Express",
    10000
)
print("Berhasil" if hasil else "Gagal")

# DELETE
print("\nHapus paket:")
hasil = paket.hapus_paket(9999)
print("Berhasil" if hasil else "Gagal")
