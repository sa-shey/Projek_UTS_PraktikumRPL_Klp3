import re
import customtkinter as ctk
import tkinter.messagebox as messagebox
from pathlib import Path

from models.user_model import UserModel
from views.login_view import LoginView
import views.register_view


class AuthController:
    def __init__(self):
        self.model = UserModel()
        self.user = None
        self.register_view = None

        ctk.set_appearance_mode("light")
        self.root = ctk.CTk(fg_color="#eff9f6")
        self.root.title("Login - SIM Laundry")
        self.root.geometry("880x620")
        self.root.resizable(False, False)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Memasang logo sebagai ikon jendela aplikasi
        path_logo = (Path(__file__).resolve().parent.parent / "assets" / "logo.ico")

        if path_logo.exists():
            self.root.iconbitmap(str(path_logo))

        self.view = LoginView(self.root)
        self.view.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)

        self.view.on_masuk = self.proses_login
        self.view.btn_daftar.configure(command=self.buka_registrasi)

    # LOGIN
    def proses_login(self, username, password):
        user = self.model.autentikasi(username, password)

        if user:
            self.user = user
            self.root.destroy()
        else:
            self.view.tampilkan_error("Username atau password salah.")

    # REGISTRASI
    def buka_registrasi(self):
        self.register_view = views.register_view.RegisterView(self.root)
        self.register_view.btn_daftar.configure(
            command=self.proses_registrasi
        )

    def proses_registrasi(self):
        nama = self.register_view.entry_nama.get().strip()
        no_telp = self.register_view.entry_no_telp.get().strip()
        alamat = self.register_view.entry_alamat.get().strip()
        username = self.register_view.entry_username.get().strip()
        password = self.register_view.entry_password.get()
        konfirmasi = self.register_view.entry_konfirmasi.get()

        # Semua kolom wajib diisi
        kolom_wajib = {
            "Nama lengkap": nama,
            "Nomor telepon": no_telp,
            "Alamat": alamat,
            "Username": username,
            "Password": password.strip(),
            "Konfirmasi password": konfirmasi.strip(),
        }

        kolom_kosong = [
            kolom for kolom, nilai in kolom_wajib.items()
            if not nilai
        ]

        if kolom_kosong:
            daftar_kosong = "\n".join(
                f"- {kolom}" for kolom in kolom_kosong
            )

            messagebox.showwarning(
                "Peringatan",
                "Semua kolom registrasi wajib diisi!\n\n"
                f"Kolom yang belum diisi:\n{daftar_kosong}"
            )
            return

        # Validasi format username:
        # Diawali huruf, memiliki angka, dan hanya berisi huruf serta angka.
        pola_username = r"(?=.*[0-9])[A-Za-z][A-Za-z0-9]*"

        if not re.fullmatch(pola_username, username):
            messagebox.showwarning(
                "Username Tidak Valid",
                "Username harus memenuhi ketentuan berikut:\n\n"
                "- Harus diawali dengan huruf.\n"
                "- Harus memiliki minimal satu angka.\n"
                "- Hanya boleh menggunakan huruf dan angka.\n"
                "- Tidak boleh menggunakan simbol atau spasi.\n\n"
                "Contoh: nisa27 atau andi123"
            )
            return

        # Validasi konfirmasi password
        if password != konfirmasi:
            messagebox.showwarning(
                "Peringatan",
                "Konfirmasi password tidak cocok!"
            )
            return

        # Username harus unik
        if self.model.username_exists(username):
            messagebox.showerror(
                "Gagal",
                "Username sudah digunakan! Silakan gunakan username lain."
            )
            return

        # Simpan akun dan data pelanggan
        berhasil = self.model.register_customer(
            nama,
            no_telp,
            alamat,
            username,
            password
        )

        if berhasil:
            messagebox.showinfo(
                "Sukses",
                "Registrasi berhasil. Silakan login."
            )
            self.register_view.destroy()

        else:
            messagebox.showerror(
                "Error",
                "Registrasi gagal disimpan. Silakan periksa koneksi database."
            )

    def run(self):
        self.root.mainloop()
        return self.user