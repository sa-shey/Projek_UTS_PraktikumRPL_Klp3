
import customtkinter as ctk

from models.paket_model import PaketModel
from models.transaksi_model import TransaksiModel


class CustomerView(ctk.CTkFrame):
    """Halaman khusus pelanggan untuk melihat paket dan status laundry."""

    def __init__(self, master, id_user, nama_pengguna="Pelanggan"):
        super().__init__(master, fg_color="transparent")

        self.id_user = id_user
        self.nama_pengguna = nama_pengguna

        self.paket_model = PaketModel()
        self.transaksi_model = TransaksiModel()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.buat_tampilan()
        self.muat_data()

    def buat_tampilan(self):
        # Judul halaman
        ctk.CTkLabel(
            self,
            text=f"Halo, {self.nama_pengguna}!",
            font=("Segoe UI", 24, "bold")
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(15, 5))

        ctk.CTkLabel(
            self,
            text="Selamat datang di halaman pelanggan SIM Laundry.",
            font=("Segoe UI", 13),
            text_color="gray"
        ).grid(row=1, column=0, sticky="w", padx=20, pady=(0, 15))

        # Area konten
        self.konten = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        self.konten.grid(
            row=2, column=0, sticky="nsew", padx=20, pady=10
        )
        self.konten.grid_columnconfigure(0, weight=1)

        # Bagian paket layanan
        self.label_paket = ctk.CTkLabel(
            self.konten,
            text="Daftar Paket Layanan",
            font=("Segoe UI", 18, "bold")
        )
        self.label_paket.grid(
            row=0, column=0, sticky="w", pady=(5, 10)
        )

        self.frame_paket = ctk.CTkFrame(
            self.konten,
            corner_radius=12
        )
        self.frame_paket.grid(
            row=1, column=0, sticky="ew", pady=(0, 25)
        )
        self.frame_paket.grid_columnconfigure(0, weight=1)

        # Bagian status laundry
        ctk.CTkLabel(
            self.konten,
            text="Status Laundry Saya",
            font=("Segoe UI", 18, "bold")
        ).grid(row=2, column=0, sticky="w", pady=(5, 10))

        self.frame_transaksi = ctk.CTkFrame(
            self.konten,
            corner_radius=12
        )
        self.frame_transaksi.grid(
            row=3, column=0, sticky="ew", pady=(0, 15)
        )
        self.frame_transaksi.grid_columnconfigure(0, weight=1)

        # Tombol muat ulang
        ctk.CTkButton(
            self.konten,
            text="Muat Ulang Data",
            command=self.muat_data,
            width=150
        ).grid(row=4, column=0, sticky="w", pady=10)

    def format_rupiah(self, nilai):
        return f"Rp {float(nilai or 0):,.0f}".replace(",", ".")

    def buat_baris(self, parent, nomor, teks, tebal=False):
        label = ctk.CTkLabel(
            parent,
            text=teks,
            font=(
                "Segoe UI",
                12,
                "bold" if tebal else "normal"
            ),
            anchor="w"
        )
        label.grid(
            row=nomor,
            column=0,
            sticky="ew",
            padx=15,
            pady=8
        )

    def tampilkan_paket(self, data_paket):
        for widget in self.frame_paket.winfo_children():
            widget.destroy()

        self.buat_baris(
            self.frame_paket,
            0,
            "Nama Paket | Jenis | Harga per Kg",
            True
        )

        if not data_paket:
            self.buat_baris(
                self.frame_paket,
                1,
                "Belum ada paket layanan tersedia."
            )
            return

        for nomor, paket in enumerate(data_paket, start=1):
            teks = (
                f"{paket.get('nama_paket', '-')}"
                f" | {paket.get('jenis', '-')}"
                f" | {self.format_rupiah(paket.get('harga_per_kg'))}"
            )
            self.buat_baris(self.frame_paket, nomor, teks)

    def tampilkan_transaksi(self, data_transaksi):
        for widget in self.frame_transaksi.winfo_children():
            widget.destroy()

        self.buat_baris(
            self.frame_transaksi,
            0,
            "ID | Tanggal Terima | Paket | Berat | Total Biaya | Status",
            True
        )

        if not data_transaksi:
            self.buat_baris(
                self.frame_transaksi,
                1,
                "Belum ada transaksi laundry untuk akun ini."
            )
            return

        for nomor, transaksi in enumerate(data_transaksi, start=1):
            tanggal = transaksi.get("tgl_terima", "-")
            if tanggal and tanggal != "-":
                tanggal = str(tanggal)

            teks = (
                f"{transaksi.get('id_transaksi', '-')}"
                f" | {tanggal}"
                f" | {transaksi.get('nama_paket', '-')}"
                f" | {transaksi.get('berat_kg', 0)} kg"
                f" | {self.format_rupiah(transaksi.get('total_biaya'))}"
                f" | {transaksi.get('status_cucian', '-')}"
            )
            self.buat_baris(self.frame_transaksi, nomor, teks)

    def muat_data(self):
        data_paket = self.paket_model.tampilkan_paket()
        data_transaksi = self.transaksi_model.get_transaksi_by_user(
            self.id_user
        )

        self.tampilkan_paket(data_paket)
        self.tampilkan_transaksi(data_transaksi)
