import tkinter as tk
import mysql.connector
import hashlib
from tkinter import messagebox
from tkinter import font as tkFont
from datetime import datetime

# === Koneksi ke database ===
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="tugas_akhir"
)
mycursor = conn.cursor()

# === Warna & Font ===
PRIMARY_COLOR = "#007ACC"
BG_COLOR = "#F5F5F5"
CARD_COLOR = "#FFFFFF"
TEXT_GRAY = "#666666"
BORDER_COLOR = "#DADADA"
FONT_FAMILY = "Segoe UI"

# === Superclass User ===
class User:
    def __init__(self, username):
        self.username = username

    def show_dashboard(self, root):
        raise NotImplementedError("Harus diimplementasikan di subclass")

# === Subclass Mahasiswa ===
class Mahasiswa(User):
    def show_dashboard(self, root):
        root.geometry("440x310")
        login_frame.pack_forget()
        main_frame = tk.Frame(root, bg=BG_COLOR)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)
        ScheduleCard(main_frame).pack(fill="both", expand=True)

# === Subclass Dosen ===
class Dosen(User):
    def show_dashboard(self, root):
        root.geometry("440x200")
        login_frame.pack_forget()
        main_frame = tk.Frame(root, bg=BG_COLOR)
        main_frame.pack(fill="both", expand=True, padx=15, pady=15)

        card = tk.Frame(main_frame, bg=CARD_COLOR, bd=1, relief="solid",
                        highlightthickness=1, highlightbackground=BORDER_COLOR, padx=15, pady=12)
        card.pack(fill="both", expand=True)

        tk.Label(card, text="👨‍🏫 Ini tampilan dosen", font=judul_font, bg=CARD_COLOR, fg=PRIMARY_COLOR).pack()

# === Card Presensi (untuk Mahasiswa) ===
class ScheduleCard(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, bg=CARD_COLOR, bd=1, relief="solid",
                         highlightthickness=1, highlightbackground=BORDER_COLOR,
                         padx=15, pady=12, **kwargs)
        self.build_widgets()

    def build_widgets(self):
        heading = tkFont.Font(family=FONT_FAMILY, size=11, weight="bold")
        normal = tkFont.Font(family=FONT_FAMILY, size=10)

        start_time, end_time = "07:00", "08:40"
        duration = datetime.strptime(end_time, "%H:%M") - datetime.strptime(start_time, "%H:%M")

        header = tk.Frame(self, bg=CARD_COLOR)
        header.pack(fill="x", pady=(0, 5))
        tk.Label(header, text=f"{start_time} - {end_time} WIB", font=heading, bg=CARD_COLOR, fg=PRIMARY_COLOR).pack(side="left")
        tk.Label(header, text=f"{int(duration.seconds//60//60)}h{(duration.seconds//60)%60:02d}m", bg=CARD_COLOR, fg=TEXT_GRAY).pack(side="right")

        tk.Label(self, text="📚 Pendidikan Agama Islam (Kelas DP)", font=heading, bg=CARD_COLOR).pack(anchor="w", pady=(0, 2))
        tk.Label(self, text="📍 RK 04 / LT 02", font=normal, fg=TEXT_GRAY, bg=CARD_COLOR).pack(anchor="w")
        tk.Label(self, text="UNIVERSITAS NEGERI MALANG - FT", font=normal, fg=TEXT_GRAY, bg=CARD_COLOR).pack(anchor="w", pady=(0, 5))

        pres_frame = tk.Frame(self, bg=CARD_COLOR)
        pres_frame.pack(fill="x", pady=(0, 5))
        tk.Label(pres_frame, text="⏰ Waktu Presensi 07:06:30", fg=PRIMARY_COLOR, font=normal, bg=CARD_COLOR).pack(side="left")
        tk.Label(pres_frame, text="Membuat rancangan penelitian", fg=TEXT_GRAY, font=normal, bg=CARD_COLOR).pack(side="right")

        btn_frame = tk.Frame(self, bg=CARD_COLOR)
        btn_frame.pack(fill="x", pady=(5, 0))
        for txt in ["Zoom", "Materi Kuliah", "MMP", "Presensi"]:
            tk.Button(btn_frame, text=txt, bg=PRIMARY_COLOR, fg="white", relief="flat", font=normal,
                      padx=10, pady=6, activebackground="#005F9E").pack(side="left", expand=True, fill="x", padx=4)

# === Fungsi Login ===
def login():
    username = entry_user.get()
    password = entry_pass.get()
    hashed = hashlib.sha256(password.encode()).hexdigest()

    mycursor.execute("SELECT role, password FROM users WHERE username = %s", (username,))
    result = mycursor.fetchone()

    if result and hashed == result[1]:
        role = result[0]
        messagebox.showinfo("Login Berhasil", f"Selamat datang, {username}!")

        # Instansiasi berdasarkan role
        if role == "mahasiswa":
            user = Mahasiswa(username)
        elif role == "dosen":
            user = Dosen(username)
        else:
            messagebox.showerror("Error", "Role tidak dikenali.")
            return

        user.show_dashboard(root)
    else:
        messagebox.showerror("Login Gagal", "Username atau password salah!")

# === Main Window ===
root = tk.Tk()
root.title("Login - Aplikasi Presensi")
root.geometry("360x240")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

judul_font = tkFont.Font(family=FONT_FAMILY, size=14, weight="bold")
normal_font = tkFont.Font(family=FONT_FAMILY, size=10)

# === Tampilan Login ===
login_frame = tk.Frame(root, bg=BG_COLOR)
login_frame.pack(pady=20)

tk.Label(login_frame, text="Silakan Login", font=judul_font, bg=BG_COLOR, fg=PRIMARY_COLOR).pack(pady=10)

form_frame = tk.Frame(login_frame, bg=BG_COLOR)
form_frame.pack()

tk.Label(form_frame, text="Username", width=10, anchor="w", bg=BG_COLOR, font=normal_font).grid(row=0, column=0, padx=5, pady=5)
entry_user = tk.Entry(form_frame, width=25, font=normal_font)
entry_user.grid(row=0, column=1, pady=5)

tk.Label(form_frame, text="Password", width=10, anchor="w", bg=BG_COLOR, font=normal_font).grid(row=1, column=0, padx=5, pady=5)
entry_pass = tk.Entry(form_frame, width=25, show="*", font=normal_font)
entry_pass.grid(row=1, column=1, pady=5)

tk.Button(login_frame, text="Login", width=20, bg=PRIMARY_COLOR, fg="white", font=normal_font,
          relief="flat", activebackground="#005F9E", command=login).pack(pady=15)

if __name__ == "__main__":
    root.mainloop()

