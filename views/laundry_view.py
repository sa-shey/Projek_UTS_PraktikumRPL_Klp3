from datetime import date
import customtkinter as ctk
from tkinter import ttk, messagebox

from config.database import Database
from models.transaksi_model import TransaksiModel
from models.paket_model import PaketModel

STATUS_CUCIAN = ["Antrean", "Proses", "Selesai", "Diambil"]
WARNA_KARTU = "#ffffff"

_TERANG = {
    "bg": "#ffffff",
    "fg": "#1a1a1a",
    "head_bg": "#e6e6e6",
    "head_fg": "#1a1a1a",
    "sel_bg": "#1f6aa5",
}


def _gaya_tabel() -> None:
    p = _TERANG
    gaya = ttk.Style()
    try:
        gaya.theme_use("clam")
    except Exception:
        pass

    gaya.configure(
        "Laundry.Treeview",
        background=p["bg"],
        fieldbackground=p["bg"],
        foreground=p["fg"],
        rowheight=26,
        borderwidth=0,
    )
    gaya.configure(
        "Laundry.Treeview.Heading",
        background=p["head_bg"],
        foreground=p["head_fg"],
        relief="flat",
        padding=(6, 6),
    )
    gaya.map(
        "Laundry.Treeview",
        background=[("selected", p["sel_bg"])],
        foreground=[("selected", "#ffffff")],
    )
    gaya.configure(
        "Laundry.Vertical.TScrollbar",
        background=p["head_bg"],
        troughcolor=p["bg"],
        bordercolor=p["bg"],
        arrowcolor=p["fg"],
    )


def bind_event(widget, event: str, fungsi) -> None:
    internal = getattr(widget, "_entry", None)
    if internal is not None:
        internal.bind(event, fungsi)


def _rp(nilai) -> str:
    return f"Rp {float(nilai or 0):,.0f}".replace(",", ".")


def _label(bapak, teks, baris=0, kolom=0, *, gaya=None, **tempat):
    label = ctk.CTkLabel(bapak, text=teks, **(gaya or {}))
    label.grid(row=baris, column=kolom, **tempat)
    return label


def _input(bapak, kelas, baris=0, kolom=0, *, gaya=None, **tempat):
    widget = kelas(bapak, **(gaya or {}))
    widget.grid(row=baris, column=kolom, **tempat)
    return widget


def _tombol(bapak, teks, perintah=None, baris=0, kolom=0, *, gaya=None, **tempat):
    tombol = ctk.CTkButton(bapak, text=teks, command=perintah, **(gaya or {}))
    tombol.grid(row=baris, column=kolom, **tempat)
    return tombol


def _tabel(bapak, kolom, *, baris=1, tinggi=3):
    pohon = ttk.Treeview(
        bapak,
        columns=tuple(k for k, _j, _l, _a in kolom),
        show="headings",
        height=tinggi,
        style="Laundry.Treeview",
    )
    for kunci, teks, lebar, jangkar in kolom:
        pohon.heading(kunci, text=teks)
        pohon.column(kunci, width=lebar, anchor=jangkar, stretch=jangkar == "w")
    pohon.grid(row=baris, column=0, sticky="nsew", padx=10, pady=(4, 10))
    return pohon


def _isi(kolom, teks) -> None:
    kolom.delete(0, "end")
    if teks not in (None, ""):
        kolom.insert(0, str(teks))


class LaundryView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.db = Database()
        self.transaksi_model = TransaksiModel()
        self.paket_model = PaketModel()

        self.data_transaksi_db = []
        self.data_paket_db = []
        self.data_pelanggan_db = []
        self.peta_pilihan_pelanggan = {}
        self.id_transaksi_terpilih = None

        _gaya_tabel()
        self._build_form()
        self._build_tabel()
        self.muat_ulang_semua()

    def _build_form(self) -> None:
        def label_kiri(teks, baris):
            _label(form, teks, baris, 0, sticky="w", padx=(10, 4), pady=2)

        def label_kanan(teks, baris):
            _label(form, teks, baris, 2, sticky="w", padx=(12, 4), pady=2)

        _label(
            self,
            "Form Transaksi Laundry",
            0,
            0,
            columnspan=5,
            gaya={"font": ("Segoe UI", 14, "bold"), "anchor": "w"},
            sticky="w",
            pady=(0, 6),
        )

        self.frame_form = ctk.CTkFrame(self, fg_color=WARNA_KARTU, corner_radius=14)
        form = self.frame_form
        form.grid(row=1, column=0, sticky="nsew", padx=(0, 12))
        form.grid_columnconfigure(0, weight=3)
        form.grid_columnconfigure(2, weight=3)

        merah = {"fg_color": "#b3261e", "hover_color": "#8f1e18"}

        label_kiri("Pelanggan (Username / Nama-ID)", 0)
        label_kanan("Paket Layanan", 0)

        # Input nama pelanggan (teks biasa, tanpa dropdown & tombol Hapus)
        self.entry_pelanggan = _input(
            form,
            ctk.CTkEntry,
            1,
            0,
<<<<<<< HEAD
            gaya={"placeholder_text": "Nama pelanggan"},
            sticky="ew",
            padx=(10, 12),
=======
            gaya={
                "state": "readonly",
                "values": ["-"],
                "command": lambda _v: self._isi_kontak(),
            },
            sticky="ew",
            padx=(10, 4),
            pady=2,
        )

        self.btn_hapus_pelanggan = _tombol(
            form,
            "Hapus",
            self.hapus_pelanggan_terpilih,
            1,
            1,
            gaya={**kecil, **merah},
            padx=(0, 12),
>>>>>>> 4e0271c (feat: update sistem SIM Laundry dan integrasi akun pelanggan)
            pady=2,
        )

        # Dropdown paket (tanpa tombol +Paket & Hapus)
        self.combo_paket = _input(
            form,
            ctk.CTkComboBox,
            1,
            2,
            columnspan=3,
            gaya={
                "state": "readonly",
                "values": ["-"],
                "command": lambda _v: self._hitung_total(),
            },
            columnspan=3,
            sticky="ew",
            padx=(12, 10),
            pady=2,
        )

        label_kiri("No. Telepon", 2)
        label_kanan("Alamat", 2)

        self.entry_telp = _input(
            form,
            ctk.CTkEntry,
            3,
            0,
            gaya={"placeholder_text": "08xxxxxxxxxx"},
            sticky="ew",
            padx=(10, 12),
            pady=2,
        )

        self.entry_alamat = _input(
            form,
            ctk.CTkEntry,
            3,
            2,
            columnspan=3,
            gaya={"placeholder_text": "Alamat lengkap pelanggan"},
            sticky="ew",
            padx=(12, 10),
            pady=2,
        )

        label_kiri("Berat (Kg)", 4)
        label_kanan("Status Cucian", 4)

        self.entry_berat = _input(
            form,
            ctk.CTkEntry,
            5,
            0,
            gaya={"placeholder_text": "Contoh: 3.5"},
            sticky="ew",
            padx=(10, 12),
            pady=2,
        )
<<<<<<< HEAD
        self.entry_berat._entry.bind("<KeyRelease>", lambda _e: self._hitung_total())
=======

        bind_event(
            self.entry_berat,
            "<KeyRelease>",
            lambda _e: self._hitung_total()
        )
>>>>>>> 4e0271c (feat: update sistem SIM Laundry dan integrasi akun pelanggan)

        self.combo_status = _input(
            form,
            ctk.CTkComboBox,
            5,
            2,
            columnspan=3,
            gaya={"state": "readonly", "values": STATUS_CUCIAN},
            sticky="ew",
            padx=(12, 10),
            pady=2,
        )

        label_kiri("Tanggal Terima", 6)
        label_kanan("Tanggal Selesai", 6)

        self.entry_terima = _input(
            form,
            ctk.CTkEntry,
            7,
            0,
            gaya={"placeholder_text": "YYYY-MM-DD"},
            sticky="ew",
            padx=(10, 12),
            pady=2,
        )

        self.entry_selesai = _input(
            form,
            ctk.CTkEntry,
            7,
            2,
            columnspan=3,
            gaya={"placeholder_text": "YYYY-MM-DD (opsional)"},
            sticky="ew",
            padx=(12, 10),
            pady=2,
        )

        self.label_total = _label(
            form,
            "Total Biaya: Rp 0",
            8,
            0,
            columnspan=5,
            gaya={"font": ("Segoe UI", 14, "bold")},
            sticky="w",
            padx=10,
            pady=(12, 2),
        )

        tombol = ctk.CTkFrame(form, fg_color="transparent")
        tombol.grid(
            row=9,
            column=0,
            columnspan=5,
            sticky="ew",
            padx=10,
            pady=(6, 12)
        )
        tombol.grid_columnconfigure((0, 1, 2), weight=1)

        aksi = {"height": 34}

        self.btn_simpan = _tombol(
            tombol,
            "Simpan Data",
            self.simpan_transaksi,
            0,
            0,
            gaya=aksi,
            sticky="ew",
            padx=(0, 4),
        )

        self.btn_perbarui = _tombol(
            tombol,
            "Perbarui",
            self.perbarui_transaksi,
            0,
            1,
            gaya={**aksi, "fg_color": "#1f6aa5"},
            sticky="ew",
            padx=4,
        )

        self.btn_hapus_transaksi = _tombol(
            tombol,
            "Hapus",
            self.hapus_transaksi,
            0,
            2,
            gaya={**aksi, **merah},
            sticky="ew",
            padx=(4, 0),
        )

    def _build_tabel(self) -> None:
        _label(
            self,
            "Daftar Transaksi",
            0,
            1,
            gaya={"font": ("Segoe UI", 14, "bold"), "anchor": "w"},
            sticky="w",
            pady=(0, 6),
        )

        self.frame_tabel = ctk.CTkFrame(
            self,
            fg_color=WARNA_KARTU,
            corner_radius=14
        )

        bingkai = self.frame_tabel
        bingkai.grid(row=1, column=1, sticky="nsew")
        bingkai.grid_rowconfigure(1, weight=1)
        bingkai.grid_columnconfigure(0, weight=1)

        self.tree = _tabel(
            bingkai,
            (
                ("id", "ID", 45, "center"),
                ("pelanggan", "Pelanggan", 150, "w"),
                ("paket", "Paket", 120, "w"),
                ("berat", "Berat", 70, "e"),
                ("total", "Total Biaya", 110, "e"),
                ("status", "Status", 90, "center"),
            ),
            tinggi=14,
        )

        self.tree.bind("<<TreeviewSelect>>", self._baris_dipilih)

        scroll = ttk.Scrollbar(
            bingkai,
            orient="vertical",
            command=self.tree.yview,
            style="Laundry.Vertical.TScrollbar",
        )
        scroll.grid(row=1, column=1, sticky="ns", padx=(0, 10), pady=(4, 6))
        self.tree.configure(yscrollcommand=scroll.set)

        _tombol(
            bingkai,
            "Muat Ulang Tampilan",
            self.muat_ulang_semua,
            2,
            0,
            columnspan=2,
            gaya={
                "height": 28,
                "fg_color": "transparent",
                "border_width": 1,
                "text_color": "gray",
            },
            sticky="ew",
            padx=10,
            pady=(0, 10),
        )

    def _ambil_pelanggan_db(self):
        """Mengambil semua pelanggan, termasuk yang belum punya akun login."""
        conn = self.db.get_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                """
                SELECT p.*, u.username, u.role
                FROM pelanggan AS p
                LEFT JOIN users AS u ON p.id_user = u.id_user
                ORDER BY u.username, p.nama, p.id_pelanggan
                """
            )
            hasil = cursor.fetchall()
            cursor.close()
            conn.close()
            return hasil

        except Exception as e:
            print(f"Error ambil pelanggan: {e}")
            conn.close()
            return []

    @staticmethod
    def _label_pelanggan(pelanggan: dict) -> str:
        """Username untuk akun terdaftar; nama + ID untuk pelanggan lama."""
        username = str(pelanggan.get("username") or "").strip()

        if username:
            return username

        return f"{pelanggan['nama']} (ID: {pelanggan['id_pelanggan']})"

    def _pelanggan_dari_pilihan(self, pilihan: str):
        """Mengambil baris pelanggan berdasarkan pilihan unik pada ComboBox."""
        return self.peta_pilihan_pelanggan.get(str(pilihan or "").strip())

    def _dapatkan_atau_buat_pelanggan(
        self,
        pilihan: str,
        telp: str,
        alamat: str
    ):
        """Mengambil ID pelanggan yang dipilih dan memperbarui data kontaknya."""
        pelanggan = self._pelanggan_dari_pilihan(pilihan)

        if not pelanggan:
            return None

        conn = self.db.get_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor()

            kolom_telp = (
                "no_telp" if "no_telp" in pelanggan else "no_telepon"
            )

            cursor.execute(
                f"UPDATE pelanggan SET {kolom_telp} = %s, alamat = %s "
                "WHERE id_pelanggan = %s",
                (telp, alamat, pelanggan["id_pelanggan"]),
            )

            conn.commit()
            id_pel = pelanggan["id_pelanggan"]

            cursor.close()
            conn.close()
            return id_pel

        except Exception as e:
            conn.rollback()
            conn.close()
            print(f"Error memperbarui data pelanggan: {e}")
            return None

    def muat_ulang_semua(self) -> None:
        self.muat_data_master()
        self.muat_daftar()

    def muat_data_master(self) -> None:
        self.data_pelanggan_db = self._ambil_pelanggan_db()
<<<<<<< HEAD
=======

        # Semua pelanggan ditampilkan.
        # Akun terdaftar memakai username.
        # Pelanggan lama memakai nama dan ID agar tidak tertukar.
        self.peta_pilihan_pelanggan = {
            self._label_pelanggan(p): p
            for p in self.data_pelanggan_db
        }

        daftar_pelanggan = (
            list(self.peta_pilihan_pelanggan.keys()) or ["-"]
        )

        self.combo_pelanggan.configure(values=daftar_pelanggan)
        self.combo_pelanggan.set(daftar_pelanggan[0])
        self._isi_kontak()
>>>>>>> 4e0271c (feat: update sistem SIM Laundry dan integrasi akun pelanggan)

        self.data_paket_db = self.paket_model.tampilkan_paket()

        daftar_paket = [
            p["nama_paket"] for p in self.data_paket_db
        ] or ["-"]

        self.combo_paket.configure(values=daftar_paket)
        self.combo_paket.set(daftar_paket[0])

        self.combo_status.configure(values=STATUS_CUCIAN)
        self.combo_status.set(STATUS_CUCIAN[0])

        _isi(self.entry_terima, date.today().isoformat())

    def muat_daftar(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.data_transaksi_db = self.transaksi_model.get_all_transaksi()

        for baris in self.data_transaksi_db:
            self.tree.insert(
                "",
                "end",
                values=(
                    baris["id_transaksi"],
                    baris["nama_pelanggan"],
                    baris["nama_paket"],
                    f"{float(baris['berat_kg']):g} kg",
                    _rp(baris["total_biaya"]),
                    baris["status_cucian"],
                ),
            )

    def _baris_dipilih(self, _event=None) -> None:
        pilihan = self.tree.selection()

        if not pilihan:
            return

        id_terpilih = self.tree.item(pilihan[0], "values")[0]
        self.id_transaksi_terpilih = id_terpilih

        for baris in self.data_transaksi_db:
            if str(baris["id_transaksi"]) != str(id_terpilih):
                continue
<<<<<<< HEAD
            _isi(self.entry_pelanggan, baris["nama_pelanggan"])
            self._isi_kontak_dari_nama(baris["nama_pelanggan"])
=======

            pelanggan = next(
                (
                    p for p in self.data_pelanggan_db
                    if str(p["id_pelanggan"]) == str(baris.get("id_pelanggan"))
                ),
                None,
            )

            self.combo_pelanggan.set(
                self._label_pelanggan(pelanggan) if pelanggan else "-"
            )

            self._isi_kontak()
>>>>>>> 4e0271c (feat: update sistem SIM Laundry dan integrasi akun pelanggan)
            self.combo_paket.set(baris["nama_paket"])

            _isi(
                self.entry_berat,
                f"{float(baris['berat_kg']):g}"
            )

            _isi(
                self.entry_terima,
                str(baris.get("tgl_terima") or "")
            )

            _isi(
                self.entry_selesai,
                str(baris.get("tgl_selesai") or "")
            )

            self.combo_status.set(baris["status_cucian"])
            self._hitung_total()
            break

    def simpan_transaksi(self) -> None:
<<<<<<< HEAD
        nama_pelanggan = self.entry_pelanggan.get().strip()
=======
        nama_pelanggan = self.combo_pelanggan.get().strip()

>>>>>>> 4e0271c (feat: update sistem SIM Laundry dan integrasi akun pelanggan)
        if not nama_pelanggan or nama_pelanggan == "-":
            messagebox.showwarning(
                "Peringatan",
                "Pilih username atau data pelanggan yang valid."
            )
            return

        telp = self.entry_telp.get().strip()
        alamat = self.entry_alamat.get().strip()

        id_pelanggan = self._dapatkan_atau_buat_pelanggan(
            nama_pelanggan,
            telp,
            alamat
        )

        if not id_pelanggan:
            messagebox.showerror(
                "Gagal",
                "Gagal mengambil atau memperbarui data pelanggan."
            )
            return

        nama_paket = self.combo_paket.get()

        paket = next(
            (
                p for p in self.data_paket_db
                if p["nama_paket"] == nama_paket
            ),
            None,
        )

        if not paket:
            messagebox.showwarning(
                "Peringatan",
                "Pilih paket layanan yang valid."
            )
            return

        try:
            berat = float(self.entry_berat.get().strip())

            if berat <= 0:
                raise ValueError

        except ValueError:
            messagebox.showwarning(
                "Peringatan",
                "Masukkan berat cucian yang valid (angka lebih dari 0)."
            )
            return

        total_biaya = berat * float(paket["harga_per_kg"])

        tgl_terima = (
            self.entry_terima.get().strip()
            or date.today().isoformat()
        )

        tgl_selesai = self.entry_selesai.get().strip() or None
        status_cucian = self.combo_status.get()

        if self.transaksi_model.create_transaksi(
            id_pelanggan,
            paket["id_paket"],
            berat,
            tgl_terima,
            tgl_selesai,
            total_biaya,
            status_cucian,
        ):
            messagebox.showinfo(
                "Sukses",
                "Data transaksi baru berhasil disimpan!"
            )

            self.id_transaksi_terpilih = None
            self._bersihkan_form()
            self.muat_ulang_semua()

        else:
            messagebox.showerror(
                "Gagal",
                "Gagal menyimpan data transaksi ke database."
            )

<<<<<<< HEAD
    # ==================================================================
    # UPDATE & DELETE TRANSAKSI
    # ==================================================================
=======
    def tambah_paket_dialog(self) -> None:
        dialog = ctk.CTkToplevel(self)
        dialog.title("Tambah Paket Layanan")
        dialog.geometry("360x320")
        dialog.resizable(False, False)
        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text="ID Paket (Contoh: PK05)"
        ).pack(anchor="w", padx=20, pady=(14, 2))

        e_id = ctk.CTkEntry(
            dialog,
            placeholder_text="PK05"
        )
        e_id.pack(fill="x", padx=20)

        ctk.CTkLabel(
            dialog,
            text="Nama Paket"
        ).pack(anchor="w", padx=20, pady=(8, 2))

        e_nama = ctk.CTkEntry(
            dialog,
            placeholder_text="Cuci Express"
        )
        e_nama.pack(fill="x", padx=20)

        ctk.CTkLabel(
            dialog,
            text="Jenis Layanan"
        ).pack(anchor="w", padx=20, pady=(8, 2))

        e_jenis = ctk.CTkEntry(
            dialog,
            placeholder_text="Kiloan / Satuan"
        )
        e_jenis.pack(fill="x", padx=20)

        ctk.CTkLabel(
            dialog,
            text="Harga per Kg (Rp)"
        ).pack(anchor="w", padx=20, pady=(8, 2))

        e_harga = ctk.CTkEntry(
            dialog,
            placeholder_text="10000"
        )
        e_harga.pack(fill="x", padx=20)

        def proses_simpan():
            id_p = e_id.get().strip()
            nama_p = e_nama.get().strip()
            jenis_p = e_jenis.get().strip() or "Kiloan"

            try:
                harga_p = float(e_harga.get().strip())

                if harga_p <= 0:
                    raise ValueError

            except ValueError:
                messagebox.showwarning(
                    "Peringatan",
                    "Harga harus berupa angka > 0.",
                    parent=dialog
                )
                return

            if not id_p or not nama_p:
                messagebox.showwarning(
                    "Peringatan",
                    "ID Paket dan Nama Paket wajib diisi.",
                    parent=dialog
                )
                return

            if self.paket_model.tambah_paket(
                id_p,
                nama_p,
                jenis_p,
                harga_p
            ):
                messagebox.showinfo(
                    "Sukses",
                    f"Paket '{nama_p}' berhasil ditambahkan.",
                    parent=dialog
                )

                dialog.destroy()
                self.muat_data_master()
                self.combo_paket.set(nama_p)
                self._hitung_total()

            else:
                messagebox.showerror(
                    "Gagal",
                    "Gagal menambah paket (pastikan ID Paket belum dipakai).",
                    parent=dialog
                )

        ctk.CTkButton(
            dialog,
            text="Simpan Paket",
            command=proses_simpan
        ).pack(fill="x", padx=20, pady=18)

>>>>>>> 4e0271c (feat: update sistem SIM Laundry dan integrasi akun pelanggan)
    def perbarui_transaksi(self) -> None:
        if not self.id_transaksi_terpilih:
            messagebox.showwarning(
                "Peringatan",
                "Klik baris transaksi pada tabel di kanan terlebih dahulu!"
            )
            return

<<<<<<< HEAD
        nama_pelanggan = self.entry_pelanggan.get().strip()
=======
        nama_pelanggan = self.combo_pelanggan.get().strip()

>>>>>>> 4e0271c (feat: update sistem SIM Laundry dan integrasi akun pelanggan)
        if not nama_pelanggan or nama_pelanggan == "-":
            messagebox.showwarning(
                "Peringatan",
                "Pilih username atau data pelanggan yang valid."
            )
            return

        telp = self.entry_telp.get().strip()
        alamat = self.entry_alamat.get().strip()

        id_pelanggan = self._dapatkan_atau_buat_pelanggan(
            nama_pelanggan,
            telp,
            alamat
        )

        if not id_pelanggan:
            messagebox.showerror(
                "Gagal",
                "Gagal mengambil atau memperbarui data pelanggan."
            )
            return

        nama_paket = self.combo_paket.get()

        paket = next(
            (
                p for p in self.data_paket_db
                if p["nama_paket"] == nama_paket
            ),
            None,
        )

        if not paket:
            messagebox.showwarning(
                "Peringatan",
                "Paket layanan tidak valid."
            )
            return

        try:
            berat = float(self.entry_berat.get().strip())

            if berat <= 0:
                raise ValueError

        except ValueError:
            messagebox.showwarning(
                "Peringatan",
                "Masukkan berat cucian yang valid (angka lebih dari 0)."
            )
            return

        total_biaya = berat * float(paket["harga_per_kg"])

        tgl_terima = (
            self.entry_terima.get().strip()
            or date.today().isoformat()
        )

        tgl_selesai = self.entry_selesai.get().strip() or None
        status_cucian = self.combo_status.get()

        if self.transaksi_model.update_transaksi(
            self.id_transaksi_terpilih,
            id_pelanggan,
            paket["id_paket"],
            berat,
            tgl_terima,
            tgl_selesai,
            total_biaya,
            status_cucian,
        ):
            messagebox.showinfo(
                "Sukses",
                f"Transaksi ID {self.id_transaksi_terpilih} berhasil diperbarui."
            )

            self.id_transaksi_terpilih = None
            self._bersihkan_form()
            self.muat_ulang_semua()

        else:
            messagebox.showerror(
                "Gagal",
                "Gagal memperbarui data transaksi ke database."
            )

    def hapus_transaksi(self) -> None:
        if not self.id_transaksi_terpilih:
            messagebox.showwarning(
                "Peringatan",
                "Klik baris transaksi pada tabel di kanan terlebih dahulu!"
            )
            return

        if not messagebox.askyesno(
            "Konfirmasi Hapus",
            f"Yakin ingin menghapus transaksi ID {self.id_transaksi_terpilih}?",
        ):
            return

        if self.transaksi_model.delete_transaksi(
            self.id_transaksi_terpilih
        ):
            messagebox.showinfo(
                "Sukses",
                "Data transaksi berhasil dihapus dari database."
            )

            self.id_transaksi_terpilih = None
            self._bersihkan_form()
            self.muat_daftar()

        else:
            messagebox.showerror(
                "Gagal",
                "Data transaksi gagal dihapus."
            )

<<<<<<< HEAD
    def _isi_kontak_dari_nama(self, nama: str) -> None:
        target = nama.strip().lower()
        for orang in self.data_pelanggan_db:
            if orang["nama"].strip().lower() == target:
                telp = orang.get("no_telp") or orang.get("no_telepon") or ""
                _isi(self.entry_telp, telp)
                _isi(self.entry_alamat, orang.get("alamat") or "")
=======
    def hapus_paket_terpilih(self) -> None:
        nama_paket = self.combo_paket.get()

        id_paket = next(
            (
                p["id_paket"] for p in self.data_paket_db
                if p["nama_paket"] == nama_paket
            ),
            None,
        )

        if not id_paket:
            messagebox.showwarning(
                "Peringatan",
                "Pilih paket layanan yang valid."
            )
            return

        if not messagebox.askyesno(
            "Konfirmasi Hapus",
            f"Yakin ingin menghapus paket '{nama_paket}'?"
        ):
            return

        if self.paket_model.hapus_paket(id_paket):
            messagebox.showinfo(
                "Sukses",
                f"Paket '{nama_paket}' berhasil dihapus."
            )
            self.muat_data_master()

        else:
            messagebox.showerror(
                "Gagal",
                f"Paket '{nama_paket}' gagal dihapus karena masih dipakai di tabel transaksi!",
            )

    def hapus_pelanggan_terpilih(self) -> None:
        pilihan = self.combo_pelanggan.get().strip()
        pelanggan = self._pelanggan_dari_pilihan(pilihan)

        if not pelanggan:
            messagebox.showwarning(
                "Peringatan",
                "Pilih pelanggan yang ingin dihapus terlebih dahulu."
            )
            return

        nama = pelanggan.get("nama", "Pelanggan")
        username = pelanggan.get("username")
        id_pelanggan = pelanggan["id_pelanggan"]

        keterangan = nama
        if username:
            keterangan += f" (username: {username})"

        if not messagebox.askyesno(
            "Konfirmasi Hapus",
            f"Yakin ingin menghapus pelanggan '{keterangan}'?\n\n"
            "Akun login customer yang terhubung juga akan dihapus."
        ):
            return

        conn = self.db.get_connection()

        if not conn:
            messagebox.showerror(
                "Gagal",
                "Tidak dapat terhubung ke database."
            )
            return

        cursor = None

        try:
            cursor = conn.cursor(dictionary=True)

            # Cek apakah pelanggan masih memiliki transaksi.
            cursor.execute(
                """
                SELECT COUNT(*) AS jumlah
                FROM transaksi_laundry
                WHERE id_pelanggan = %s
                """,
                (id_pelanggan,),
            )

            hasil = cursor.fetchone()
            jumlah_transaksi = int(hasil["jumlah"] or 0)

            if jumlah_transaksi > 0:
                conn.rollback()

                messagebox.showwarning(
                    "Pelanggan Masih Memiliki Transaksi",
                    f"Pelanggan '{nama}' masih memiliki "
                    f"{jumlah_transaksi} transaksi.\n"
                    "Hapus transaksi terkait terlebih dahulu "
                    "sebelum menghapus pelanggan."
                )
>>>>>>> 4e0271c (feat: update sistem SIM Laundry dan integrasi akun pelanggan)
                return

            id_user = pelanggan.get("id_user")
            role = pelanggan.get("role")

            # Hapus data pelanggan.
            cursor.execute(
                """
                DELETE FROM pelanggan
                WHERE id_pelanggan = %s
                """,
                (id_pelanggan,),
            )

            if cursor.rowcount == 0:
                conn.rollback()

                messagebox.showerror(
                    "Gagal",
                    "Data pelanggan tidak ditemukan."
                )
                return

            # Hapus akun login jika terhubung dengan role customer.
            if id_user and role == "customer":
                cursor.execute(
                    """
                    DELETE FROM users
                    WHERE id_user = %s AND role = 'customer'
                    """,
                    (id_user,),
                )

            conn.commit()

            pesan = f"Pelanggan '{nama}' berhasil dihapus."

            if id_user and role == "customer":
                pesan += " Akun loginnya juga telah dihapus."

            messagebox.showinfo("Sukses", pesan)

            self.id_transaksi_terpilih = None
            self._bersihkan_form()
            self.muat_ulang_semua()

        except Exception as e:
            conn.rollback()

            messagebox.showerror(
                "Gagal",
                f"Pelanggan gagal dihapus.\nDetail: {e}"
            )

        finally:
            if cursor:
                cursor.close()
            conn.close()

    def _isi_kontak(self) -> None:
        pilihan = self.combo_pelanggan.get().strip()
        orang = self._pelanggan_dari_pilihan(pilihan)

        if orang:
            telp = (
                orang.get("no_telp")
                or orang.get("no_telepon")
                or ""
            )

            _isi(self.entry_telp, telp)
            _isi(self.entry_alamat, orang.get("alamat") or "")
            return

        _isi(self.entry_telp, "")
        _isi(self.entry_alamat, "")

    def _bersihkan_form(self) -> None:
        _isi(self.entry_pelanggan, "")
        _isi(self.entry_berat, "")
        _isi(self.entry_selesai, "")
        _isi(self.entry_telp, "")
        _isi(self.entry_alamat, "")
        self.label_total.configure(text="Total Biaya: Rp 0")

    def _hitung_total(self) -> None:
        harga = 0

        for paket in self.data_paket_db:
            if paket["nama_paket"] == self.combo_paket.get():
                harga = float(paket["harga_per_kg"])
                break

        try:
            berat = float(self.entry_berat.get().strip() or 0)

        except ValueError:
            berat = 0
<<<<<<< HEAD
        self.label_total.configure(text=f"Total Biaya: {_rp(berat * harga)}")

=======

        self.label_total.configure(
            text=f"Total Biaya: {_rp(berat * harga)}"
        )
>>>>>>> 4e0271c (feat: update sistem SIM Laundry dan integrasi akun pelanggan)
