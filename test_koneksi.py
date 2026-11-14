
from config.database import Database

db = Database()
koneksi = db.get_connection()

if koneksi:
    print("Database db_laundry berhasil terhubung!")
    koneksi.close()
else:
    print("Database belum berhasil terhubung.")
