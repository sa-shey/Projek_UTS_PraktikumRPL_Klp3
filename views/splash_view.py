from pathlib import Path
import customtkinter as ctk
from PIL import Image, ImageSequence


class SplashScreen(ctk.CTk):
    """Jendela splash screen yang memutar animasi logo dari assets/splash.gif."""

    def __init__(self) -> None:
        super().__init__(fg_color="#eff9f6")

        # Hilangkan bingkai window (borderless) & selalu di atas
        self.overrideredirect(True)
        self.attributes("-topmost", True)

        lebar, tinggi = 460, 340
        x = (self.winfo_screenwidth() - lebar) // 2
        y = (self.winfo_screenheight() - tinggi) // 2
        self.geometry(f"{lebar}x{tinggi}+{x}+{y}")

        # Kartu pembungkus
        kartu = ctk.CTkFrame(
            self,
            fg_color="#ffffff",
            corner_radius=20,
            border_width=2,
            border_color="#0d9488",
        )
        kartu.pack(fill="both", expand=True, padx=4, pady=4)

        # Label tempat menampilkan frame animasi
        self.lbl_animasi = ctk.CTkLabel(kartu, text="")
        self.lbl_animasi.pack(pady=(16, 8))

        ctk.CTkLabel(
            kartu,
            text="SIMO-JL",
            font=("Segoe UI", 20, "bold"),
            text_color="#0f3d38",
        ).pack()

        ctk.CTkLabel(
            kartu,
            text="Memuat Sistem Informasi Manajemen Operasional Jasa Laundry...",
            font=("Segoe UI", 11),
            text_color="#5f8a84",
        ).pack(pady=(2, 12))

        # Muat seluruh frame dari assets/splash.gif
        akar_proyek = Path(__file__).resolve().parent.parent
        path_gif = akar_proyek / "assets" / "splash.gif"

        self.frames = []
        self.delay = 60

        if path_gif.exists():
            gif = Image.open(path_gif)
            self.delay = gif.info.get("duration", 60)
            for frame in ImageSequence.Iterator(gif):
                rgba = frame.convert("RGBA")
                ctk_img = ctk.CTkImage(
                    light_image=rgba, dark_image=rgba, size=(420, 236)
                )
                self.frames.append(ctk_img)

        self.indeks = 0
        self._putar_frame()

    def _putar_frame(self) -> None:
        if self.indeks < len(self.frames):
            self.lbl_animasi.configure(image=self.frames[self.indeks])
            self.indeks += 1
            self.after(self.delay, self._putar_frame)
        else:
            # Tahan 0.5 detik di frame logo utuh lalu masuk ke Login
            self.after(500, self.destroy)