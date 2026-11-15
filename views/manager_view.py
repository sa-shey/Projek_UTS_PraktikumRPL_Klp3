import customtkinter as ctk
from tkinter import ttk, messagebox

from models.paket_model import PaketModel


class ManagerView(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.paket_model = PaketModel()
        self.data_paket = []
        self.id_paket_terpilih = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        self.buat_tampilan()
        self.muat_data()

    def buat_tampilan(self):
        ctk.CTkLabel(
            self,
            text="Manajemen Paket Layanan",
            font=("Segoe UI", 24, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=15,
            pady=(10, 5)
        )

        ctk.CTkLabel(
            self,
            text="Tambah, ubah, dan hapus paket layanan laundry.",
            font=("Segoe UI", 13),
            text_color="gray"
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=15,
            pady=(0, 15)
        )

        # Form paket
        self.frame_form = ctk.CTkFrame(
            self,
            corner_radius=12
        )
        self.frame_form.grid(
            row=2,
            column=0,
            sticky="new",
            padx=15,
            pady=5
        )
        self.frame_form.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            self.frame_form,
            text="Form Paket Layanan",
            font=("Segoe UI", 17, "bold")
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            padx=15,
            pady=(15, 10)
        )

        self.entry_id = self.buat_input("ID Paket", 1)
        self.entry_nama = self.buat_input("Nama Paket", 2)
        self.entry_jenis = self.buat_input("Jenis Layanan", 3)
        self.entry_harga = self.buat_input("Harga per Kg", 4)

        tombol = ctk.CTkFrame(
            self.frame_form,
            fg_color="transparent"
        )
        tombol.grid(
            row=5,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=15,
            pady=15
        )

        tombol.grid_columnconfigure(
            (0, 1, 2, 3),
            weight=1
        )

        ctk.CTkButton(
            tombol,
            text="Tambah Paket",
            command=self.tambah_paket
        ).grid(
            row=0,
            column=0,
            padx=4,
            sticky="ew"
        )

        ctk.CTkButton(
            tombol,
            text="Ubah Paket",
            command=self.ubah_paket,
            fg_color="#1f6aa5"
        ).grid(
            row=0,
            column=1,
            padx=4,
            sticky="ew"
        )

        ctk.CTkButton(
            tombol,
            text="Hapus Paket",
            command=self.hapus_paket,
            fg_color="#b3261e",
            hover_color="#8f1e18"
        ).grid(
            row=0,
            column=2,
            padx=4,
            sticky="ew"
        )

        ctk.CTkButton(
            tombol,
            text="Bersihkan",
            command=self.bersihkan_form,
            fg_color="gray"
        ).grid(
            row=0,
            column=3,
            padx=4,
            sticky="ew"
        )

        # Tabel paket
        self.frame_tabel = ctk.CTkFrame(
            self,
            corner_radius=12
        )
        self.frame_tabel.grid(
            row=3,
            column=0,
            sticky="nsew",
            padx=15,
            pady=10
        )

        self.frame_tabel.grid_columnconfigure(0, weight=1)
        self.frame_tabel.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(
            self.frame_tabel,
            text="Daftar Paket Layanan",
            font=("Segoe UI", 17, "bold")
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=15,
            pady=10
        )

        self.tabel = ttk.Treeview(
            self.frame_tabel,
            columns=("id", "nama", "jenis", "harga"),
            show="headings",
            height=10
        )

        self.tabel.heading("id", text="ID Paket")
        self.tabel.heading("nama", text="Nama Paket")
        self.tabel.heading("jenis", text="Jenis Layanan")
        self.tabel.heading("harga", text="Harga per Kg")

        self.tabel.column("id", width=100, anchor="center")
        self.tabel.column("nama", width=200)
        self.tabel.column("jenis", width=150)
        self.tabel.column("harga", width=150, anchor="e")

        self.tabel.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=15,
            pady=(0, 10)
        )

        self.tabel.bind(
            "<<TreeviewSelect>>",
            self.pilih_paket
        )

        ctk.CTkButton(
            self.frame_tabel,
            text="Muat Ulang Data",
            command=self.muat_data,
            width=150
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=15,
            pady=(0, 15)
        )

    def buat_input(self, placeholder, baris):
        ctk.CTkLabel(
            self.frame_form,
            text=placeholder
        ).grid(
            row=baris,
            column=0,
            sticky="w",
            padx=15,
            pady=5
        )

        entry = ctk.CTkEntry(
            self.frame_form,
            placeholder_text=placeholder
        )
        entry.grid(
            row=baris,
            column=1,
            sticky="ew",
            padx=15,
            pady=5
        )

        return entry

    def format_rupiah(self, nilai):
        return f"Rp {float(nilai or 0):,.0f}".replace(",", ".")

    def muat_data(self):
        for item in self.tabel.get_children():
            self.tabel.delete(item)

        self.data_paket = self.paket_model.tampilkan_paket()

        for paket in self.data_paket:
            self.tabel.insert(
                "",
                "end",
                values=(
                    paket["id_paket"],
                    paket["nama_paket"],
                    paket["jenis"],
                    self.format_rupiah(paket["harga_per_kg"])
                )
            )

    def pilih_paket(self, event=None):
        pilihan = self.tabel.selection()

        if not pilihan:
            return

        nilai = self.tabel.item(pilihan[0], "values")

        self.id_paket_terpilih = nilai[0]

        self.entry_id.configure(state="normal")
        self.entry_id.delete(0, "end")
        self.entry_id.insert(0, nilai[0])
        self.entry_id.configure(state="disabled")

        self.entry_nama.delete(0, "end")
        self.entry_nama.insert(0, nilai[1])

        self.entry_jenis.delete(0, "end")
        self.entry_jenis.insert(0, nilai[2])

        self.entry_harga.delete(0, "end")

        harga = next(
            (
                p["harga_per_kg"]
                for p in self.data_paket
                if str(p["id_paket"]) == str(nilai[0])
            ),
            ""
        )

        self.entry_harga.insert(0, str(harga))

    def tambah_paket(self):
        id_paket = self.entry_id.get().strip()
        nama = self.entry_nama.get().strip()
        jenis = self.entry_jenis.get().strip()

        try:
            harga = float(self.entry_harga.get().strip())

            if harga <= 0:
                raise ValueError

        except ValueError:
            messagebox.showwarning(
                "Peringatan",
                "Harga harus berupa angka lebih dari 0."
            )
            return

        if not id_paket or not nama or not jenis:
            messagebox.showwarning(
                "Peringatan",
                "Semua kolom wajib diisi."
            )
            return

        berhasil = self.paket_model.tambah_paket(
            id_paket,
            nama,
            jenis,
            harga
        )

        if berhasil:
            messagebox.showinfo(
                "Sukses",
                "Paket layanan berhasil ditambahkan."
            )
            self.bersihkan_form()
            self.muat_data()

        else:
            messagebox.showerror(
                "Gagal",
                "Paket gagal ditambahkan. Periksa ID paket atau koneksi database."
            )

    def ubah_paket(self):
        if not self.id_paket_terpilih:
            messagebox.showwarning(
                "Peringatan",
                "Pilih paket pada tabel terlebih dahulu."
            )
            return

        nama = self.entry_nama.get().strip()
        jenis = self.entry_jenis.get().strip()

        try:
            harga = float(self.entry_harga.get().strip())

            if harga <= 0:
                raise ValueError

        except ValueError:
            messagebox.showwarning(
                "Peringatan",
                "Harga harus berupa angka lebih dari 0."
            )
            return

        if not nama or not jenis:
            messagebox.showwarning(
                "Peringatan",
                "Nama dan jenis layanan wajib diisi."
            )
            return

        berhasil = self.paket_model.update_paket(
            self.id_paket_terpilih,
            nama,
            jenis,
            harga
        )

        if berhasil:
            messagebox.showinfo(
                "Sukses",
                "Paket layanan berhasil diperbarui."
            )
            self.bersihkan_form()
            self.muat_data()

        else:
            messagebox.showerror(
                "Gagal",
                "Paket gagal diperbarui."
            )

    def hapus_paket(self):
        if not self.id_paket_terpilih:
            messagebox.showwarning(
                "Peringatan",
                "Pilih paket pada tabel terlebih dahulu."
            )
            return

        konfirmasi = messagebox.askyesno(
            "Konfirmasi",
            "Apakah kamu yakin ingin menghapus paket ini?"
        )

        if not konfirmasi:
            return

        berhasil = self.paket_model.hapus_paket(
            self.id_paket_terpilih
        )

        if berhasil:
            messagebox.showinfo(
                "Sukses",
                "Paket layanan berhasil dihapus."
            )
            self.bersihkan_form()
            self.muat_data()

        else:
            messagebox.showerror(
                "Gagal",
                "Paket tidak dapat dihapus. Mungkin masih digunakan oleh transaksi."
            )

    def bersihkan_form(self):
        self.id_paket_terpilih = None

        self.entry_id.configure(state="normal")
        self.entry_id.delete(0, "end")

        self.entry_nama.delete(0, "end")
        self.entry_jenis.delete(0, "end")
        self.entry_harga.delete(0, "end")

        for item in self.tabel.selection():
            self.tabel.selection_remove(item)