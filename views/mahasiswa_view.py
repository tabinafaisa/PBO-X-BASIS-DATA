import ttkbootstrap as ttk
from tkinter import *
from tkinter import messagebox, Toplevel
from datetime import datetime
from models.database import get_jadwal_mahasiswa_hari_ini, insert_presensi
from PIL import Image, ImageTk
import os
from models.database import get_connection

class MahasiswaView:
    def __init__(self, root, id_user):
        self.root = root
        self.id_user = id_user
        self.root.title("Jadwal Kuliah Mahasiswa")
        self.root.configure(bg="white")

        # === Header ===
        header_frame = ttk.Frame(root, padding=10)
        header_frame.pack(fill=X)
        header_frame.configure(style="Header.TFrame")
        style = ttk.Style()
        style.configure("Header.TFrame", background="#ffffff")

        # Logo kiri
        logo_path = "assets/logo.png"
        logo_img = Image.open(logo_path).resize((40, 40))
        logo_photo = ImageTk.PhotoImage(logo_img)
        logo_label = ttk.Label(header_frame, image=logo_photo, style="Header.TLabel")
        logo_label.image = logo_photo
        logo_label.pack(side=LEFT, padx=(0, 10))

        # Spacer agar header tidak padat
        Frame(header_frame, bg="#f0f0f0").pack(side=LEFT, expand=True)

        # Profil kanan
        profile_frame = ttk.Frame(header_frame, style="Header.TFrame")
        profile_frame.pack(side=RIGHT)
        profile_info_frame = ttk.Frame(profile_frame, style="Header.TFrame")
        profile_info_frame.pack(side=RIGHT)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Nama FROM mahasiswa WHERE id_user = %s", (id_user,))
        nama_mhs = cursor.fetchone()[0]
        conn.close()

        profile_info_frame = ttk.Frame(profile_frame, style="Header.TFrame")
        profile_info_frame.pack(side=RIGHT)

        # Foto profil
        profil_path = "assets/profile.png"
        profil_img = Image.open(profil_path).resize((40, 40))
        profil_photo = ImageTk.PhotoImage(profil_img)
        profil_label = Label(profile_info_frame, image=profil_photo, bg="#ffffff")
        profil_label.image = profil_photo
        profil_label.pack(side=RIGHT, padx=5)

        ttk.Label(profile_info_frame, text=nama_mhs, font=("Helvetica", 10, "bold"),
                background="#ffffff").pack(side=RIGHT, padx=5, anchor="e")

        # Konten utama
        self.content_frame = Frame(root, padx=20, pady=20)
        self.content_frame.pack(fill=BOTH, expand=True)

        jadwal_hari_ini = get_jadwal_mahasiswa_hari_ini(id_user)

        # Tombol logout di kanan bawah
        logout_frame = Frame(root, bg="white")
        logout_frame.place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)
        logout_btn = Button(logout_frame, text="Logout", bg="#ff0000", fg="white", padx=10, pady=5, command=self.logout)
        logout_btn.pack()

        if not jadwal_hari_ini:
            empty_frame = Frame(self.content_frame, pady=50)
            empty_frame.pack(fill=BOTH, expand=True)

            empty_img_path = os.path.join("assets", "no_schedule.png")
            if os.path.exists(empty_img_path):
                img = Image.open(empty_img_path).resize((180, 180))
                self.empty_photo = ImageTk.PhotoImage(img)
                Label(empty_frame, image=self.empty_photo).pack(pady=(0, 20))

            Label(empty_frame, text="Yay! Tidak ada jadwal kuliah hari ini.", font=("Segoe UI", 14, "bold")).pack()
            Label(empty_frame, text="Gunakan waktumu untuk istirahat, belajar, atau hal produktif lainnya 👌", 
                  font=("Segoe UI", 10), wraplength=400, justify="center").pack(pady=10)
            return

        for item in jadwal_hari_ini:
            self.tampilkan_jadwal(item)

    def tampilkan_jadwal(self, data):
        frame = Frame(self.content_frame, bd=2, relief="solid", padx=10, pady=10)
        frame.pack(pady=10, fill=X)

        jam_mulai = str(data['Jam_mulai'])[:5] if data['Jam_mulai'] else '--:--'
        jam_selesai = str(data['Jam_selesai'])[:5] if data['Jam_selesai'] else '--:--'
        durasi = self.hitung_durasi(data['Jam_mulai'], data['Jam_selesai'])

        Label(frame, text=f"{jam_mulai} - {jam_selesai} WIB ({durasi})", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        Label(frame, text=data['Nama_MK'], font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(5, 0))
        Label(frame, text=f"\U0001F3EB Kelas: {data['Nama_Kelas']}", font=("Segoe UI", 10)).pack(anchor="w")
        Label(frame, text=f"\U0001F464 Dosen: {data['Nama_Dosen']}", font=("Segoe UI", 10)).pack(anchor="w")
        Label(frame, text="UNIVERSITAS NEGERI MALANG - FT", font=("Segoe UI", 9, "italic")).pack(anchor="w", pady=(0, 5))

        waktu_presensi = data['Waktu_presensi'] if data['Waktu_presensi'] else '--:--:--'
        Label(frame, text=f"\u23F1 Waktu Presensi: {waktu_presensi}", fg="blue", font=("Segoe UI", 9)).pack(anchor="w")

        sudah_presensi = data['Waktu_presensi'] is not None
        btn_state = "disabled" if sudah_presensi else "normal"
        Button(frame, text="Presensi", bg="green", fg="white", padx=20,
               state=btn_state,
               command=lambda: self.dialog_status_presensi(
                    data['ID_Pertemuan'],
                    data['NIM'],
                    data['Jam_mulai'],
                    data['Jam_selesai']
                )).pack(pady=(10, 0))

    def hitung_durasi(self, jam_mulai, jam_selesai):
        try:
            if not jam_mulai or not jam_selesai:
                return "--:--"
            mulai = datetime.strptime(str(jam_mulai), "%H:%M:%S")
            selesai = datetime.strptime(str(jam_selesai), "%H:%M:%S")
            durasi = selesai - mulai
            total_menit = durasi.total_seconds() // 60
            jam = int(total_menit // 60)
            menit = int(total_menit % 60)
            return f"{jam}h{menit}m"
        except Exception:
            return "Durasi tidak valid"

    def boleh_presensi(self, jam_mulai_str, jam_selesai_str):
        now = datetime.now().time()
        jam_mulai = datetime.strptime(str(jam_mulai_str), "%H:%M:%S").time()
        jam_selesai = datetime.strptime(str(jam_selesai_str), "%H:%M:%S").time()
        return jam_mulai <= now <= jam_selesai

    def dialog_status_presensi(self, id_pertemuan, nim, jam_mulai, jam_selesai):
        if not self.boleh_presensi(jam_mulai, jam_selesai):
            messagebox.showwarning("Diluar Waktu", "Presensi hanya bisa dilakukan dalam rentang jam kuliah.")
            return

        popup = Toplevel(self.root)
        popup.title("Pilih Status Presensi")
        popup.geometry("300x200")
        popup.grab_set()

        Label(popup, text="Pilih status presensi:", font=("Segoe UI", 11, "bold")).pack(pady=10)

        def pilih(status):
            try:
                insert_presensi(nim, id_pertemuan, status)
                messagebox.showinfo("Presensi", f"Presensi ({status}) berhasil!")
                popup.destroy()
                self.refresh_view()
            except Exception as e:
                messagebox.showerror("Presensi Gagal", f"Gagal melakukan presensi:\n{e}")

        for kode, label in [('H', 'Hadir'), ('I', 'Izin'), ('S', 'Sakit'), ('A', 'Alpa')]:
            Button(popup, text=label, width=15, command=lambda s=kode: pilih(s)).pack(pady=5)

    def refresh_view(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        MahasiswaView(self.root, self.id_user)

    def logout(self):
        from views.login_view import LoginWindow
        for widget in self.root.winfo_children():
            widget.destroy()
        LoginWindow(self.root, None)
