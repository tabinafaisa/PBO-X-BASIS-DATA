import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from ttkbootstrap import Frame, Label, Entry, Checkbutton
from PIL import Image, ImageTk
from utils.db import get_connection
from utils.hashing import hash_password


class LoginWindow:
    def __init__(self, master, on_login_success):
        self.master = master
        self.on_login_success = on_login_success
        self.master.title("Login - Aplikasi Presensi Digital")
        self.master.state('zoomed')  # Fullscreen tapi tetap ada tombol X dan -

        # Background label
        self.bg_label = Label(self.master)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.master.after(300, self.load_background_image)
        self.master.configure(background="black")
        self.build_ui()

    def load_background_image(self):
        try:
            bg_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets", "bg1.png"))

            screen_width = self.master.winfo_screenwidth()
            screen_height = self.master.winfo_screenheight()

            image = Image.open(bg_path)
            image = image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)

            self.bg_photo = ImageTk.PhotoImage(image)
            self.bg_label.config(image=self.bg_photo)
            self.bg_label.image = self.bg_photo
            self.bg_label.lower()
        except Exception as e:
            print("Gagal load background:", e)

    def build_ui(self):
        self.container = ttk.Frame(self.master, style="TFrame")
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        form_frame = ttk.Frame(self.container, style="TFrame", padding=30)
        form_frame.pack()

        ttk.Label(form_frame, text="Aplikasi Presensi Digital",
                  font=("Helvetica", 16, "bold")).pack(pady=10)

        ttk.Label(form_frame, text="Username").pack(anchor="w")
        self.username_entry = ttk.Entry(form_frame, width=30)
        self.username_entry.pack(pady=5)

        ttk.Label(form_frame, text="Password").pack(anchor="w")
        self.password_entry = ttk.Entry(form_frame, width=30, show="*")
        self.password_entry.pack(pady=5)

        self.show_password = ttk.BooleanVar()
        ttk.Checkbutton(form_frame, text="Tampilkan Password", variable=self.show_password,
                        command=self.toggle_password).pack(anchor="w", pady=5)

        ttk.Button(form_frame, text="Login", bootstyle="primary", width=30,
                   command=self.proses_login).pack(pady=(10, 5))

        ttk.Button(self.master, text="⯺ Kembali", bootstyle="secondary-outline",
                   command=lambda: self.master.state('normal')).place(x=10, y=10)

    def toggle_password(self):
        self.password_entry.config(show="" if self.show_password.get() else "*")

    def fade_in(self, window, alpha=0.0):
        if alpha < 1.0:
            alpha += 0.1
            window.wm_attributes("-alpha", alpha)
            window.after(30, lambda: self.fade_in(window, alpha))
        else:
            window.wm_attributes("-alpha", 1.0)

    def show_custom_error(self, message):
        error_window = ttk.Toplevel(self.master)
        error_window.title("Kesalahan")
        error_window.configure(background="white")

        popup_width = 300
        popup_height = 180

        window_width = self.master.winfo_width()
        window_height = self.master.winfo_height()
        x_root = self.master.winfo_rootx()
        y_root = self.master.winfo_rooty()

        x = x_root + (window_width // 2) - (popup_width // 2)
        y = y_root + (window_height // 2) - (popup_height // 2)
        error_window.geometry(f"{popup_width}x{popup_height}+{x}+{y}")
        error_window.wm_attributes("-alpha", 0.0)
        self.fade_in(error_window)

        # Ikon Emoji ❌
        ttk.Label(error_window, text="❌", font=("Helvetica", 32), background="white", foreground="red").pack(pady=(10, 0))

        ttk.Label(error_window, text=message, background="white", font=("Helvetica", 12)).pack(pady=10)

        ttk.Button(error_window, text="Tutup", command=error_window.destroy, bootstyle="danger").pack(pady=(0, 10))
        error_window.grab_set()

    def proses_login(self):
        username = self.username_entry.get()
        password = hash_password(self.password_entry.get())

        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT ID_User, role FROM users WHERE username=%s AND password=%s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            if result:
                id_user, role = result["ID_User"], result["role"]
                self.on_login_success(id_user, role)
            else:
                self.show_custom_error("Username atau password salah.")

            conn.close()
        except Exception as e:
            self.show_custom_error(f"Database Error: {str(e)}")
