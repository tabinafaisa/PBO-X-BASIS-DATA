from tkinter import *
from tkinter import messagebox, simpledialog
from datetime import datetime
from models.database import get_jadwal_mahasiswa_hari_ini
import mysql.connector

class MahasiswaView:
    def __init__(self, root, id_user):
        self.root = root
        self.id_user = id_user
        self.root.title("Jadwal Hari Ini")

        self.frame = Frame(root, padx=20, pady=20, bg="#f0f0f0")
        self.frame.pack(fill=BOTH, expand=True)

        jadwal_hari_ini = get_jadwal_mahasiswa_hari_ini(id_user)

        if not jadwal_hari_ini:
            Label(self.frame, text="Tidak ada jadwal kuliah hari ini.", font=("Segoe UI", 12)).pack()
            return

        for item in jadwal_hari_ini:
            self.tampilkan_jadwal(item)

    def tampilkan_jadwal(self, data):
        frame = Frame(self.frame, bd=1, relief="solid", padx=12, pady=12, bg="white")
        frame.pack(pady=10, padx=15, fill=X)

        jam_mulai = data['Jam_mulai'][:5]
        jam_selesai = data['Jam_selesai'][:5]
        waktu_mulai = datetime.strptime(data['Jam_mulai'], "%H:%M:%S")
        waktu_selesai = datetime.strptime(data['Jam_selesai'], "%H:%M:%S")
        durasi = waktu_selesai - waktu_mulai

        durasi = waktu_selesai - waktu_mulai
        durasi_str = str(durasi).rsplit(":", 1)[0]  # Aman, hasilnya '1:40'
        Label(
            frame,
            text=f"{jam_mulai} - {jam_selesai} WIB ({durasi_str})",
            font=("Segoe UI", 10, "bold"),
            bg="white"
        ).pack(anchor="w")

        Label(frame, text=data['Nama_MK'], font=("Segoe UI", 12, "bold"), bg="white", fg="#2c3e50").pack(anchor="w", pady=(5, 0))
        Label(frame, text=f"\U0001F3EB Kelas: {data['Nama_Kelas']}", font=("Segoe UI", 10), bg="white").pack(anchor="w")
        Label(frame, text=f"\U0001F464 Dosen: {data['Nama_Dosen']}", font=("Segoe UI", 10), bg="white").pack(anchor="w")
        Label(frame, text="UNIVERSITAS NEGERI MALANG - FT", font=("Segoe UI", 9, "italic"), fg="#555", bg="white").pack(anchor="w", pady=(0, 5))

        waktu_presensi = data['Waktu_presensi'] or '--:--:--'
        Label(frame, text=f"\u23F1 Waktu Presensi: {waktu_presensi}", fg="blue", font=("Segoe UI", 9), bg="white").pack(anchor="w", pady=(0, 5))

        Button(frame, text="Presensi", bg="green", fg="white", padx=20, command=lambda: self.presensi(data['ID_Pertemuan'])).pack()

    def presensi(self, id_pertemuan):
        pilihan = simpledialog.askstring("Presensi", "Masukkan status (H: Hadir, I: Izin, S: Sakit, A: Alfa):")

        if pilihan and pilihan.upper() in ['H', 'I', 'S', 'A']:
            waktu = datetime.now().strftime("%H:%M:%S")
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="tugas_akhir"
                )
                cursor = conn.cursor()

                cursor.execute("SELECT NIM FROM mahasiswa WHERE Id_user = %s", (self.id_user,))
                result = cursor.fetchone()
                if not result:
                    messagebox.showerror("Error", "NIM mahasiswa tidak ditemukan.")
                    return
                nim = result[0]

                cursor.execute("""
                    INSERT INTO presensi (NIM, ID_Pertemuan, Waktu_presensi, Kode_Status)
                    VALUES (%s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE Waktu_presensi=%s, Kode_Status=%s
                """, (nim, id_pertemuan, waktu, pilihan.upper(), waktu, pilihan.upper()))

                conn.commit()
                conn.close()
                messagebox.showinfo("Presensi", "Presensi berhasil disimpan.")
                self.frame.destroy()
                self.__init__(self.root, self.id_user)

            except mysql.connector.Error as e:
                messagebox.showerror("Database Error", str(e))
        else:
            messagebox.showwarning("Presensi", "Input tidak valid. Gunakan H, I, S, atau A.")
