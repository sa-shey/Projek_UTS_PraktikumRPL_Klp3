import customtkinter as ctk
import tkinter.messagebox as messagebox
from models.user_model import UserModel
from views.login_view import LoginView
from views.register_view import RegisterView


class AuthController:
    def __init__(self):
        self.model = UserModel()
        self.user = None            # diisi saat login berhasil
        self.register_view = None

        # Jendela utama untuk halaman login (LoginView adalah Frame,
        # jadi butuh jendela CTk sebagai wadahnya).
        ctk.set_appearance_mode("light")
        self.root = ctk.CTk(fg_color="#eff9f6")
        self.root.title("Login - SIM Laundry")
        self.root.geometry("880x620")
        self.root.resizable(False, False)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.view = LoginView(self.root)
        self.view.grid(row=0, column=0, sticky="nsew", padx=16, pady=16)

        # Menghubungkan View dengan Controller
        self.view.on_masuk = self.proses_login
        self.view.btn_daftar.configure(command=self.buka_registrasi)

    # ------------------------------------------------------------------
    # LOGIN
    # ------------------------------------------------------------------
    def proses_login(self, username, password):
        user = self.model.autentikasi(username, password)
        if user:
            self.user = user
            self.root.destroy()     # menutup login; run() membuka jendela utama
        else:
            self.view.tampilkan_error("Username atau password salah.")

    # ------------------------------------------------------------------
    # REGISTRASI
    # ------------------------------------------------------------------
    def buka_registrasi(self):
        self.register_view = RegisterView(self.root)
        self.register_view.btn_daftar.configure(command=self.proses_registrasi)

    def proses_registrasi(self):
        username = self.register_view.entry_username.get().strip()
        password = self.register_view.entry_password.get()
        konfirmasi = self.register_view.entry_konfirmasi.get()

        if not username or not password or not konfirmasi:
            messagebox.showwarning("Peringatan", "Semua kolom wajib diisi!")
            return
        if password != konfirmasi:
            messagebox.showwarning("Peringatan", "Konfirmasi password tidak cocok!")
            return
        if self.model.username_exists(username):
            messagebox.showerror("Gagal", "Username sudah digunakan!")
            return

        # Role dikunci 'user' di sini, bukan dari input form
        if self.model.register_user(username, password, role="user"):
            messagebox.showinfo("Sukses", "Registrasi berhasil. Silakan login.")
            self.register_view.destroy()
        else:
            messagebox.showerror("Error", "Registrasi gagal disimpan.")

    # ------------------------------------------------------------------
    def run(self):
        """Menampilkan jendela login. Mengembalikan dict {id_user, username, role}
        jika login berhasil, atau None jika jendela ditutup tanpa login."""
        self.root.mainloop()
        return self.user