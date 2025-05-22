from tkinter import *
from tkinter import messagebox
from datetime import datetime
from models.database import get_jadwal_mahasiswa_hari_ini, insert_presensi

class MahasiswaView:
    def __init__(self, root, id_user):
        self.root = root
        self.root.title("Jadwal Kuliah Hari Ini")
        self.frame = Frame(root, padx=20, pady=20)
        self.frame.pack()

        jadwal_hari_ini = get_jadwal_mahasiswa_hari_ini(id_user)

        print("MahasiswaView dimulai")
        jadwal_hari_ini = get_jadwal_mahasiswa_hari_ini(id_user)
        print("Jadwal:", jadwal_hari_ini)

        if not jadwal_hari_ini:
            Label(self.frame, text="Tidak ada jadwal kuliah hari ini.", font=("Segoe UI", 12)).pack()
            return

        for item in jadwal_hari_ini:
            self.tampilkan_jadwal(item)

    def tampilkan_jadwal(self, data):
        frame = Frame(self.frame, bd=2, relief="solid", padx=10, pady=10)
        frame.pack(pady=10, fill=X)

        jam_mulai = str(data['Jam_mulai'])[:5]
        jam_selesai = str(data['Jam_selesai'])[:5]
        durasi = self.hitung_durasi(data['Jam_mulai'], data['Jam_selesai'])

        Label(frame, text=f"{jam_mulai} - {jam_selesai} WIB ({durasi})", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        Label(frame, text=data['Nama_MK'], font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(5, 0))
        Label(frame, text=f"🏫 Kelas: {data['Nama_Kelas']}", font=("Segoe UI", 10)).pack(anchor="w")
        Label(frame, text=f"👤 Dosen: {data['Nama_Dosen']}", font=("Segoe UI", 10)).pack(anchor="w")
        Label(frame, text="UNIVERSITAS NEGERI MALANG - FT", font=("Segoe UI", 9, "italic")).pack(anchor="w", pady=(0, 5))

        waktu_presensi = data['Waktu_presensi'] if data['Waktu_presensi'] else '--:--:--'
        Label(frame, text=f"⏱ Waktu Presensi: {waktu_presensi}", fg="blue", font=("Segoe UI", 9)).pack(anchor="w")

        sudah_presensi = data['Waktu_presensi'] is not None
        btn_state = "disabled" if sudah_presensi else "normal"
        Button(frame, text="Presensi", bg="green", fg="white", padx=20,
               state=btn_state,
               command=lambda: self.presensi(data['ID_Pertemuan'], data['NIM'])).pack(pady=(10, 0))

    def hitung_durasi(self, jam_mulai, jam_selesai):
        try:
            mulai = datetime.strptime(str(jam_mulai), "%H:%M:%S")
            selesai = datetime.strptime(str(jam_selesai), "%H:%M:%S")
            durasi = selesai - mulai
            total_menit = durasi.total_seconds() // 60
            jam = int(total_menit // 60)
            menit = int(total_menit % 60)
            return f"{jam}h{menit}m"
        except Exception as e:
            return "Durasi tidak valid"

    def presensi(self, id_pertemuan, nim):
        try:
            insert_presensi(nim, id_pertemuan)
            messagebox.showinfo("Presensi", "Presensi berhasil dilakukan!")
            self.frame.destroy()  # Refresh frame biar tombol disable
            MahasiswaView(self.root, self.id_user)
        except Exception as e:
            messagebox.showerror("Presensi Gagal", f"Gagal melakukan presensi:\n{e}")
