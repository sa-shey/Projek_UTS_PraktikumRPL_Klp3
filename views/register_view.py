import customtkinter as ctk


class RegisterView(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("Registrasi - SIM Laundry")
        self.geometry("420x680")
        self.resizable(False, False)

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(
            pady=15,
            padx=20,
            fill="both",
            expand=True
        )

        ctk.CTkLabel(
            self.frame,
            text="REGISTRASI PELANGGAN",
            font=("Arial", 18, "bold")
        ).pack(pady=(15, 5))

        ctk.CTkLabel(
            self.frame,
            text="Semua kolom bertanda (*) wajib diisi.",
            font=("Arial", 11),
            text_color="gray"
        ).pack(pady=(0, 10))

        self.entry_nama = ctk.CTkEntry(
            self.frame,
            placeholder_text="Nama Lengkap *"
        )
        self.entry_nama.pack(
            pady=7,
            padx=20,
            fill="x"
        )

        self.entry_no_telp = ctk.CTkEntry(
            self.frame,
            placeholder_text="Nomor Telepon *"
        )
        self.entry_no_telp.pack(
            pady=7,
            padx=20,
            fill="x"
        )

        self.entry_alamat = ctk.CTkEntry(
            self.frame,
            placeholder_text="Alamat Lengkap *"
        )
        self.entry_alamat.pack(
            pady=7,
            padx=20,
            fill="x"
        )

        self.entry_username = ctk.CTkEntry(
            self.frame,
            placeholder_text="Username (contoh: nisa27) *"
        )
        self.entry_username.pack(
            pady=7,
            padx=20,
            fill="x"
        )

        ctk.CTkLabel(
            self.frame,
            text="Username harus berisi huruf dan angka.",
            font=("Arial", 11),
            text_color="gray"
        ).pack(pady=(0, 5))

        self.entry_password = ctk.CTkEntry(
            self.frame,
            placeholder_text="Password *",
            show="*"
        )
        self.entry_password.pack(
            pady=7,
            padx=20,
            fill="x"
        )

        self.entry_konfirmasi = ctk.CTkEntry(
            self.frame,
            placeholder_text="Konfirmasi Password *",
            show="*"
        )
        self.entry_konfirmasi.pack(
            pady=7,
            padx=20,
            fill="x"
        )

        self.btn_daftar = ctk.CTkButton(
            self.frame,
            text="Daftar"
        )
        self.btn_daftar.pack(
            pady=(18, 10),
            padx=20,
            fill="x"
        )