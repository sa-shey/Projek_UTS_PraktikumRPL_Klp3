from datetime import date

try:
    from controller.auth_controller import AuthController, ROLE_ADMIN
except ImportError:
    AuthController = None
    ROLE_ADMIN = "Admin"

from models.pelanggan_model import PelangganModel
from models.paket_model import PaketModel
from models.transaksi_model import TransaksiModel

STATUS_CUCIAN = ("Antrean", "Proses", "Selesai", "Diambil")
AKUN = {"atmin": "atmin123"}


class LaundryController:
    def __init__(
        self,
        pelanggan_model=None,
        paket_model=None,
        transaksi_model=None,
        auth_controller=None,
        current_user=None,
    ):
        self.pelanggan_model = pelanggan_model or PelangganModel()
        self.paket_model = paket_model or PaketModel()
        self.transaksi_model = transaksi_model or TransaksiModel()
        if auth_controller is not None:
            self.auth_controller = auth_controller
        elif AuthController is not None:
            try:
                self.auth_controller = AuthController()
            except Exception:
                self.auth_controller = None
        else:
            self.auth_controller = None
        self.current_user = current_user

    def set_user(self, user):
        self.current_user = user

    def role_pengguna(self) -> str:
        if isinstance(self.current_user, dict):
            return str(self.current_user.get("role") or "User")
        return "Admin" if self.current_user else "Admin"

    def nama_pengguna(self) -> str:
        if isinstance(self.current_user, dict):
            return str(self.current_user.get("username") or "Pengguna")
        return str(self.current_user or "Pengguna")

    def apakah_admin(self) -> bool:
        if self.current_user is None:
            return True
        if isinstance(self.current_user, dict):
            return self.current_user.get("role") == ROLE_ADMIN
        return str(self.current_user) in ("atmin", "Admin")

    def ambil_pelanggan(self):
        data = self.pelanggan_model.get_all_pelanggan()
        return sorted(data, key=lambda d: str(d["nama"]).lower())

    def ambil_paket(self):
        data = self.paket_model.get_all_paket()
        return sorted(data, key=lambda d: str(d["nama_paket"]).lower())

    def ambil_status(self):
        return STATUS_CUCIAN

    def ambil_transaksi(self):
        nomor = {p["id_pelanggan"]: p.get("no_telp") for p in self.pelanggan_model.get_all_pelanggan()}
        data = self.transaksi_model.get_all_transaksi()
        for t in data:
            t["no_telp_pelanggan"] = nomor.get(t["id_pelanggan"])
        return sorted(data, key=lambda d: d["id_transaksi"], reverse=True)

    def ambil_kontak_pelanggan(self):
        transaksi = self.transaksi_model.get_all_transaksi()
        hasil = []
        for p in self.pelanggan_model.get_all_pelanggan():
            milik = [t for t in transaksi if t["id_pelanggan"] == p["id_pelanggan"]]
            hasil.append({
                "id_pelanggan": p["id_pelanggan"],
                "nama": p["nama"],
                "no_telp": p.get("no_telp"),
                "alamat": p.get("alamat"),
                "jumlah_transaksi": len(milik),
                "total_belanja": sum(float(t["total_biaya"] or 0) for t in milik),
            })
        return sorted(hasil, key=lambda d: str(d["nama"]).lower())

    def ringkasan(self):
        pelanggan = self.pelanggan_model.get_all_pelanggan()
        paket = self.paket_model.get_all_paket()
        transaksi = self.transaksi_model.get_all_transaksi()

        status = {s: 0 for s in STATUS_CUCIAN}
        berat, pendapatan = 0.0, 0.0
        hari_ini, pendapatan_hari_ini = 0, 0.0
        hari = date.today().isoformat()

        for t in transaksi:
            if t["status_cucian"] in status:
                status[t["status_cucian"]] += 1
            nilai = float(t["total_biaya"] or 0)
            berat += float(t["berat_kg"] or 0)
            pendapatan += nilai
            if str(t["tgl_terima"]) == hari:
                hari_ini += 1
                pendapatan_hari_ini += nilai

        return {
            "total_pelanggan": len(pelanggan),
            "total_paket": len(paket),
            "total_transaksi": len(transaksi),
            "total_pendapatan": pendapatan,
            "st_antrean": status["Antrean"],
            "st_proses": status["Proses"],
            "st_selesai": status["Selesai"],
            "st_diambil": status["Diambil"],
            "trx_hari_ini": hari_ini,
            "pendapatan_hari_ini": pendapatan_hari_ini,
            "total_berat": berat,
            "rata_berat": round(berat / len(transaksi), 1) if transaksi else 0,
            "pelanggan_kontak": sum(1 for p in pelanggan if p.get("no_telp")),
        }

    def detail_pelanggan(self, nama):
        target = str(nama or "").strip().lower()
        for p in self.pelanggan_model.get_all_pelanggan():
            if str(p["nama"]).strip().lower() == target:
                return p
        return None

    def cari_id_paket(self, nama):
        target = str(nama or "").strip().lower()
        for k in self.paket_model.get_all_paket():
            if str(k["nama_paket"]).strip().lower() == target:
                return k["id_paket"]
        return None

    def harga_paket(self, id_paket):
        for k in self.paket_model.get_all_paket():
            if k["id_paket"] == id_paket:
                return float(k["harga_per_kg"] or 0)
        return 0.0

    def hitung_total(self, berat_kg, id_paket):
        if not id_paket:
            return 0.0
        try:
            berat = float(berat_kg)
            return round(berat * self.harga_paket(id_paket), 2) if berat > 0 else 0.0
        except (TypeError, ValueError):
            return 0.0

    def _validasi_transaksi(self, id_pelanggan, id_paket, berat_kg, tgl_terima, status_cucian):
        if not id_pelanggan:
            return False, "Pelanggan wajib dipilih."
        if not id_paket:
            return False, "Paket layanan wajib dipilih."
        if status_cucian not in STATUS_CUCIAN:
            return False, "Status cucian tidak valid."
        try:
            if float(berat_kg) <= 0:
                return False, "Berat cucian harus lebih besar dari nol."
        except (TypeError, ValueError):
            return False, "Berat cucian harus berupa angka."
        if not str(tgl_terima or "").strip():
            return False, "Tanggal terima wajib diisi."
        return True, ""

    def simpan(self, id_transaksi, id_pelanggan, id_paket, berat_kg, tgl_terima, tgl_selesai, status_cucian):
        if id_transaksi:
            return self.perbarui(
                id_transaksi, id_pelanggan, id_paket, berat_kg, tgl_terima, tgl_selesai, status_cucian
            )

        valid, pesan = self._validasi_transaksi(id_pelanggan, id_paket, berat_kg, tgl_terima, status_cucian)
        if not valid:
            return False, pesan

        total = self.hitung_total(berat_kg, id_paket)
        tgl_selesai_clean = str(tgl_selesai or "").strip() or None

        ok = self.transaksi_model.create_transaksi(
            int(id_pelanggan), int(id_paket), float(berat_kg),
            str(tgl_terima).strip(), tgl_selesai_clean, total, status_cucian
        )
        return (True, "Transaksi berhasil disimpan.") if ok else (False, "Transaksi gagal disimpan.")

    def perbarui(self, id_transaksi, id_pelanggan, id_paket, berat_kg, tgl_terima, tgl_selesai, status_cucian):
        if not self.apakah_admin():
            return False, "Akses ditolak: hanya Admin yang dapat memperbarui transaksi."
        if not id_transaksi:
            return False, "ID transaksi wajib dipilih."

        valid, pesan = self._validasi_transaksi(id_pelanggan, id_paket, berat_kg, tgl_terima, status_cucian)
        if not valid:
            return False, pesan

        total = self.hitung_total(berat_kg, id_paket)
        tgl_selesai_clean = str(tgl_selesai or "").strip() or None

        ok = self.transaksi_model.update_transaksi(
            int(id_transaksi), int(id_pelanggan), int(id_paket), float(berat_kg),
            str(tgl_terima).strip(), tgl_selesai_clean, total, status_cucian
        )
        return (True, "Transaksi berhasil diperbarui.") if ok else (
            False, "Transaksi tidak ditemukan atau gagal diperbarui."
        )

    def hapus(self, id_transaksi):
        if not self.apakah_admin():
            return False, "Akses ditolak: hanya Admin yang dapat menghapus transaksi."
        if self.transaksi_model.delete_transaksi(int(id_transaksi)):
            return True, "Transaksi berhasil dihapus."
        return False, "Transaksi tidak ditemukan."

    def pastikan_pelanggan(self, nama, no_telp="", alamat=""):
        nama = str(nama or "").strip()
        if not nama:
            return False, "Pelanggan wajib dipilih atau diketik.", None

        ada = self.detail_pelanggan(nama)
        if ada is None:
            if not self.pelanggan_model.create_pelanggan(
                nama, str(no_telp or "").strip(), str(alamat or "").strip()
            ):
                return False, "Pelanggan gagal disimpan.", None
            ada = self.detail_pelanggan(nama)
            if ada is None:
                return False, "Pelanggan gagal disimpan.", None
            return True, f"Pelanggan '{nama}' ditambahkan otomatis.", ada["id_pelanggan"]

        if (no_telp or alamat) and not (ada.get("no_telp") and ada.get("alamat")):
            self.pelanggan_model.update_pelanggan(
                ada["id_pelanggan"], ada["nama"],
                ada.get("no_telp") or str(no_telp).strip(),
                ada.get("alamat") or str(alamat).strip(),
            )
        return True, "Pelanggan ditemukan.", ada["id_pelanggan"]

    def hapus_pelanggan(self, id_pelanggan):
        if not self.apakah_admin():
            return False, "Akses ditolak: hanya Admin yang dapat menghapus pelanggan."
        target = next(
            (p for p in self.pelanggan_model.get_all_pelanggan() if p["id_pelanggan"] == int(id_pelanggan)),
            None,
        )
        if target is None:
            return False, "Pelanggan tidak ditemukan."

        jumlah = sum(1 for t in self.transaksi_model.get_all_transaksi() if t["id_pelanggan"] == int(id_pelanggan))
        if not self.pelanggan_model.delete_pelanggan(int(id_pelanggan)):
            return False, "Gagal menghapus pelanggan."

        pesan = f"Pelanggan '{target['nama']}' berhasil dihapus."
        if jumlah:
            pesan += f" {jumlah} transaksi ikut terhapus."
        return True, pesan

    def tambah_paket(self, nama_paket, jenis, harga_per_kg):
        if not self.apakah_admin():
            return False, "Akses ditolak: hanya Admin yang dapat menambah paket layanan."
        if not (nama_paket or "").strip():
            return False, "Nama paket wajib diisi."
        if not (jenis or "").strip():
            return False, "Jenis layanan wajib diisi."
        try:
            if float(harga_per_kg) <= 0:
                return False, "Harga per kg harus lebih besar dari nol."
        except (TypeError, ValueError):
            return False, "Harga per kg harus berupa angka."

        if self.paket_model.create_paket(str(nama_paket).strip(), str(jenis).strip(), float(harga_per_kg)):
            return True, "Paket berhasil ditambahkan."
        return False, "Paket gagal disimpan."

    def hapus_paket(self, id_paket):
        if not self.apakah_admin():
            return False, "Akses ditolak: hanya Admin yang dapat menghapus paket layanan."
        target = next(
            (k for k in self.paket_model.get_all_paket() if k["id_paket"] == int(id_paket)),
            None,
        )
        if target is None:
            return False, "Paket layanan tidak ditemukan."

        jumlah = sum(1 for t in self.transaksi_model.get_all_transaksi() if t["id_paket"] == int(id_paket))
        if not self.paket_model.delete_paket(int(id_paket)):
            return False, "Gagal menghapus paket."

        pesan = f"Paket '{target['nama_paket']}' berhasil dihapus."
        if jumlah:
            pesan += f" {jumlah} transaksi ikut terhapus."
        return True, pesan

    def login(self, username, password):
        if self.auth_controller is not None:
            ok, pesan, user = self.auth_controller.login(username, password)
            if ok:
                self.current_user = user
            return ok, pesan, user

        username = str(username or "").strip()
        password = str(password or "")
        if not username or not password:
            return False, "Username dan password wajib diisi.", None

        if AKUN.get(username) == password:
            user = {"id_user": 1, "username": username, "role": ROLE_ADMIN}
            self.current_user = user
            return True, f"Selamat datang, {username}!", user

        return False, "Username atau password salah.", None
