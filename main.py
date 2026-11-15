import sys
import platform
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent))

import customtkinter as ctk
from PIL import Image, ImageTk

from controller.auth_controller import AuthController
from views.dashboard_view import DashboardView
from views.laundry_view import LaundryView, _label, _tombol
from views.customer_view import CustomerView
from views.manager_view import ManagerView
from views.splash_view import SplashScreen


JUDUL = "SIM Laundry - Sistem Informasi Manajemen Operasional Jasa Laundry"
AKAR_PROYEK = Path(__file__).resolve().parent
PATH_LOGO_ICO = AKAR_PROYEK / "assets" / "logo.ico"
PATH_LOGO_PNG = AKAR_PROYEK / "assets" / "logo.png"

LATAR = "#eff9f6"
SIDE = "#ffffff"
MINT = "#0d9488"
MINT_GELAP = "#0f766e"
MINT_MUDA = "#ccfbf1"
TEKS = "#0f3d38"
TEKS_LUNAK = "#5f8a84"
MERAH = "#f43f5e"


# ==================================================================
# UTILITAS
# ==================================================================

def terapkan_tema() -> None:
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")


def muat_gambar_logo(ukuran: tuple[int, int]):
    path_aktif = (
        PATH_LOGO_ICO if PATH_LOGO_ICO.exists()
        else PATH_LOGO_PNG
    )

    if not path_aktif.exists():
        return None

    img_pil = Image.open(path_aktif).convert("RGBA")
    return ctk.CTkImage(
        light_image=img_pil,
        dark_image=img_pil,
        size=ukuran
    )


def pasang_ikon_jendela(jendela) -> None:
    path_aktif = (
        PATH_LOGO_ICO if PATH_LOGO_ICO.exists()
        else PATH_LOGO_PNG
    )

    if not path_aktif.exists():
        return

    try:
        if platform.system() == "Windows" and PATH_LOGO_ICO.exists():
            jendela.iconbitmap(str(PATH_LOGO_ICO))
        else:
            ikon_pil = Image.open(path_aktif).convert("RGBA")
            ikon_tk = ImageTk.PhotoImage(ikon_pil)
            jendela.wm_iconphoto(True, ikon_tk)
            jendela._ikon_ref = ikon_tk
    except Exception:
        pass


def tampilkan_splash() -> None:
    splash = SplashScreen()
    splash.mainloop()


def buka_jendela_login() -> dict:
    pengguna = AuthController().run()

    if pengguna is None:
        raise SystemExit

    return pengguna


# ==================================================================
# SIDEBAR
# ==================================================================

def _sidebar(bangunan, pengguna, role, daftar_menu, aktif):
    sisi = ctk.CTkFrame(
        bangunan,
        width=232,
        corner_radius=0,
        fg_color=SIDE
    )
    sisi.pack(side="left", fill="y")
    sisi.grid_propagate(False)
    sisi.grid_columnconfigure(0, weight=1)
    sisi.grid_rowconfigure(5, weight=1)

    logo_img = muat_gambar_logo((68, 68))

    if logo_img is not None:
        lbl_logo = ctk.CTkLabel(
            sisi,
            image=logo_img,
            text=""
        )
        lbl_logo.image = logo_img
        lbl_logo.grid(row=0, column=0, pady=(24, 2))
    else:
        _label(
            sisi,
            "🧺",
            0,
            0,
            gaya={"font": ("Segoe UI", 30)},
            pady=(24, 0)
        )

    _label(
        sisi,
        "SIM Laundry",
        1,
        0,
        gaya={
            "font": ("Segoe UI", 18, "bold"),
            "text_color": TEKS
        },
        pady=(4, 0)
    )

    _label(
        sisi,
        "Manajemen Operasional\nJasa Laundry",
        2,
        0,
        gaya={
            "font": ("Segoe UI", 11),
            "text_color": TEKS_LUNAK,
            "justify": "center"
        },
        pady=(2, 20)
    )

    menu = {}

    for baris, (nama, ikon) in enumerate(daftar_menu, start=3):
        terpilih = nama == aktif

        menu[nama] = _tombol(
            sisi,
            f"  {ikon}   {nama}",
            None,
            baris,
            0,
            gaya={
                "anchor": "w",
                "corner_radius": 12,
                "height": 44,
                "font": ("Segoe UI", 13, "bold"),
                "hover_color": MINT_MUDA,
                "border_width": 0,
                "fg_color": (
                    MINT_MUDA if terpilih else "transparent"
                ),
                "text_color": (
                    MINT_GELAP if terpilih else TEKS
                )
            },
            sticky="ew",
            padx=14,
            pady=4
        )

    kartu = ctk.CTkFrame(
        sisi,
        fg_color=LATAR,
        corner_radius=12
    )
    kartu.grid(
        row=6,
        column=0,
        sticky="ew",
        padx=14,
        pady=(0, 20)
    )

    _label(
        kartu,
        "Pengguna",
        0,
        0,
        gaya={
            "font": ("Segoe UI", 10),
            "text_color": TEKS_LUNAK,
            "anchor": "w"
        }
    ).grid(sticky="ew", padx=12, pady=(8, 0))

    _label(
        kartu,
        pengguna,
        1,
        0,
        gaya={
            "font": ("Segoe UI", 13, "bold"),
            "text_color": TEKS,
            "anchor": "w"
        }
    ).grid(sticky="ew", padx=12, pady=(0, 2))

    _label(
        kartu,
        role,
        2,
        0,
        gaya={
            "font": ("Segoe UI", 10),
            "text_color": TEKS_LUNAK,
            "anchor": "w"
        }
    ).grid(sticky="ew", padx=12, pady=(0, 8))

    tombol_keluar = _tombol(
        kartu,
        "Keluar",
        None,
        3,
        0,
        gaya={
            "height": 32,
            "corner_radius": 10,
            "fg_color": "transparent",
            "border_width": 1,
            "border_color": MERAH,
            "text_color": MERAH,
            "font": ("Segoe UI", 12, "bold")
        }
    )
    tombol_keluar.grid(
        sticky="ew",
        padx=12,
        pady=(0, 10)
    )

    return menu, tombol_keluar


# ==================================================================
# JENDELA UTAMA BERDASARKAN ROLE
# ==================================================================

def buka_jendela_utama(
    pengguna: str,
    role: str = "user",
    id_user=None
) -> bool:

    # Menentukan aktor berdasarkan role akun.
    if role == "customer":
        nama_role = "Pelanggan"
        daftar_menu = [
            ("Paket dan Status Laundry", "🧺")
        ]

    elif role == "user":
        nama_role = "Kasir / Operator"
        daftar_menu = [
            ("Dashboard", "📊"),
            ("Transaksi Laundry", "🧺")
        ]

    elif role == "admin":
        nama_role = "Manajer / Pemilik"
        daftar_menu = [
            ("Dashboard", "📊"),
            ("Manajemen Paket Layanan", "📦")
        ]

    else:
        raise ValueError(f"Role pengguna tidak dikenal: {role}")

    halaman_awal = daftar_menu[0][0]

    jendela = ctk.CTk(fg_color=LATAR)
    jendela.title(JUDUL)
    jendela.geometry("1260x780+20+20")
    jendela.minsize(1040, 620)
    pasang_ikon_jendela(jendela)

    menu, tombol_keluar = _sidebar(
        jendela,
        pengguna,
        nama_role,
        daftar_menu,
        halaman_awal
    )

    # Area konten utama
    konten = ctk.CTkFrame(
        jendela,
        fg_color=LATAR,
        corner_radius=0
    )
    konten.pack(side="right", fill="both", expand=True)

    konten.grid_rowconfigure(1, weight=1)
    konten.grid_columnconfigure(0, weight=1)

    _label(
        konten,
        "Selamat datang di Sistem Informasi "
        "Manajemen Operasional Jasa Laundry",
        0,
        0,
        gaya={
            "font": ("Segoe UI", 12),
            "text_color": TEKS_LUNAK,
            "anchor": "w"
        },
        sticky="ew",
        padx=22,
        pady=(18, 8)
    )

    wadah = ctk.CTkFrame(
        konten,
        fg_color=LATAR
    )
    wadah.grid(
        row=1,
        column=0,
        sticky="nsew",
        padx=22,
        pady=(0, 18)
    )

    wadah.grid_rowconfigure(0, weight=1)
    wadah.grid_columnconfigure(0, weight=1)

    # Menyiapkan halaman sesuai role.
    halaman = {}

    if role == "customer":
        if id_user is None:
            raise ValueError(
                "ID pengguna tidak ditemukan untuk akun pelanggan."
            )

        view_customer = CustomerView(
            wadah,
            id_user,
            pengguna
        )

        view_customer.configure(fg_color=LATAR)
        view_customer.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        halaman["Paket dan Status Laundry"] = view_customer

    elif role == "user":
        view_dashboard = DashboardView(wadah, pengguna)
        view_transaksi = LaundryView(wadah)

        view_dashboard.configure(fg_color=LATAR)
        view_transaksi.configure(fg_color=LATAR)

        view_dashboard.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        view_transaksi.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        view_dashboard.btn_refresh.configure(
            fg_color=MINT,
            hover_color=MINT_GELAP
        )

        view_transaksi.grid_rowconfigure(1, weight=1)
        view_transaksi.grid_columnconfigure(1, weight=1)

        halaman["Dashboard"] = view_dashboard
        halaman["Transaksi Laundry"] = view_transaksi

    elif role == "admin":
        view_dashboard = DashboardView(wadah, pengguna)
        view_manager = ManagerView(wadah)

        view_dashboard.configure(fg_color=LATAR)
        view_manager.configure(fg_color=LATAR)

        view_dashboard.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        view_manager.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        view_dashboard.btn_refresh.configure(
            fg_color=MINT,
            hover_color=MINT_GELAP
        )

        halaman["Dashboard"] = view_dashboard
        halaman["Manajemen Paket Layanan"] = view_manager

    # Fungsi untuk berpindah halaman.
    def tampilkan(nama):
        for kunci, tombol in menu.items():
            terpilih = kunci == nama

            tombol.configure(
                fg_color=(
                    MINT_MUDA if terpilih else "transparent"
                ),
                text_color=(
                    MINT_GELAP if terpilih else TEKS
                )
            )

        halaman[nama].tkraise()

    for nama, tombol in menu.items():
        tombol.configure(
            command=lambda n=nama: tampilkan(n)
        )

    # Fungsi logout.
    status = {"logout": False}

    def keluar():
        status["logout"] = True
        jendela.destroy()

    tombol_keluar.configure(command=keluar)

    tampilkan(halaman_awal)

    jendela.mainloop()

    return status["logout"]


# ==================================================================
# TITIK MASUK PROGRAM
# ==================================================================

def main():
    terapkan_tema()
    tampilkan_splash()

    while True:
        try:
            pengguna = buka_jendela_login()
        except SystemExit:
            return

        logout = buka_jendela_utama(
            pengguna["username"],
            pengguna["role"],
            pengguna["id_user"]
        )

        if not logout:
            break


if __name__ == "__main__":
    main()