import tkinter as tk
from tkinter import font
from datetime import datetime

class ScheduleCard(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, bd=1, relief="solid", padx=10, pady=10, **kwargs)
        self.build_widgets()

    def build_widgets(self):
        # Waktu dan Durasi
        header = tk.Frame(self)
        header.pack(fill="x", pady=(0,5))
        start_time = "07:00"
        end_time   = "08:40"
        duration = datetime.strptime(end_time, "%H:%M") - datetime.strptime(start_time, "%H:%M")
        tk.Label(header, text=start_time + " - " + end_time + " WIB",
                 font=font.Font(size=10, weight="bold")).pack(side="left")
        tk.Label(header, text=f"{int(duration.seconds//60//60)}h{(duration.seconds//60)%60:02d}m",
                 fg="gray").pack(side="right")

        # Judul Matakuliah
        tk.Label(self, text="📚 Pendidikan Agama Islam (Kelas DP)",
                 font=font.Font(size=12, weight="bold")).pack(anchor="w")

        # Lokasi
        tk.Label(self, text="📍 RK 04 / LT 02",
                 fg="gray").pack(anchor="w")

        # Dosen / Fakultas
        tk.Label(self, text="UNIVERSITAS NEGERI MALANG - FT",
                 fg="gray").pack(anchor="w", pady=(0,5))

        # Waktu Presensi & Kegiatan
        pres_frame = tk.Frame(self)
        pres_frame.pack(fill="x", pady=(0,5))
        tk.Label(pres_frame, text="⏰ Waktu Presensi 07:06:30", fg="#0066CC").pack(side="left")
        tk.Label(pres_frame, text="Membuat rancangan penelitian", fg="gray").pack(side="right")

        # Tombol aksi
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill="x", pady=(5,0))
        for txt in ["Zoom", "Materi Kuliah", "MMP", "Presensi"]:
            btn = tk.Button(btn_frame, text=txt, relief="ridge", padx=8, pady=4)
            btn.pack(side="left", expand=True, fill="x", padx=2)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Jadwal Hari Ini")
    # atur ukuran jendela
    root.geometry("400x260")
    card = ScheduleCard(root)
    card.pack(padx=10, pady=10, fill="both", expand=True)
    root.mainloop()
