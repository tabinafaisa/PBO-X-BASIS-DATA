from tkinter import *
from tkinter import messagebox, Toplevel
from datetime import datetime
from models.database import get_jadwal_mahasiswa_hari_ini, insert_presensi

class MahasiswaView:
    def __init__(self, root, id_user):
        self.root = root
        self.id_user = id_user
        self.root.title("Jadwal Kuliah Hari Ini")
        self.frame = Frame(root, padx=20, pady=20)
        self.frame.pack()

        jadwal_hari_ini = get_jadwal_mahasiswa_hari_ini(id_user)

        print("MahasiswaView dimulai")
        print("Jadwal:", jadwal_hari_ini)

        if not jadwal_hari_ini:
            Label(self.frame, text="Tidak ada jadwal kuliah hari ini.", font=("Segoe UI", 12)).pack()
            return

        for item in jadwal_hari_ini:
            self.tampilkan_jadwal(item)

    def tampilkan_jadwal(self, data):
        frame = Frame(self.frame, bd=2, relief="solid", padx=10, pady=10)
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
               command=lambda: self.dialog_status_presensi(data['ID_Pertemuan'], data['NIM'])).pack(pady=(10, 0))

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
        except Exception as e:
            return "Durasi tidak valid"

    def dialog_status_presensi(self, id_pertemuan, nim):
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
                self.frame.destroy()
                MahasiswaView(self.root, self.id_user)
            except Exception as e:
                messagebox.showerror("Presensi Gagal", f"Gagal melakukan presensi:\n{e}")

        for kode, label in [('H', 'Hadir'), ('I', 'Izin'), ('S', 'Sakit'), ('A', 'Alpa')]:
            Button(popup, text=label, width=15, command=lambda s=kode: pilih(s)).pack(pady=5)
