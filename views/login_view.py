import tkinter as tk
from tkinter import messagebox, Frame, Label, Entry, Button, Checkbutton, BooleanVar, W, X, CENTER, SOLID
from utils.db import get_connection
from utils.hashing import hash_password

class LoginWindow:
    def __init__(self, master, on_login_success):
        self.master = master
        self.on_login_success = on_login_success
        self.master.title("Login - Aplikasi Presensi Digital")
        self.master.attributes('-fullscreen', True)
        self.master.config(bg="#F5F5F5")

        self.build_ui()

    def build_ui(self):
        main_frame = Frame(self.master, bg="white")
        main_frame.pack(expand=True, fill='both')

        form_frame = Frame(main_frame, bg="white", bd=2, relief=SOLID, padx=30, pady=30)
        form_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

        Label(form_frame, text="Aplikasi Presensi Digital", font=("Helvetica", 16, "bold"), bg="white").pack(pady=10)

        Label(form_frame, text="Username", bg="white").pack(anchor=W)
        self.username_entry = Entry(form_frame)
        self.username_entry.pack(fill=X, pady=5)

        Label(form_frame, text="Password", bg="white").pack(anchor=W)
        self.password_entry = Entry(form_frame, show="*")
        self.password_entry.pack(fill=X, pady=5)

        self.show_password = BooleanVar()
        Checkbutton(form_frame, text="Tampilkan Password", bg="white", variable=self.show_password,
                    command=self.toggle_password).pack(anchor=W, pady=5)

        Button(form_frame, text="Login", bg="#2980b9", fg="white", width=20, command=self.proses_login).pack(pady=10)

        Button(self.master, text="⯺ Kembali", command=lambda: self.master.attributes('-fullscreen', False)).place(x=10, y=10)

    def toggle_password(self):
        if self.show_password.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

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
                user_id, role = result["ID_User"], result["role"]
                print(f"Login berhasil: {user_id} - {role}")
                self.on_login_success(user_id, role)  # Jangan destroy dulu
            else:
                messagebox.showerror("Login Gagal", "Username atau password salah.")

            conn.close()

        except Exception as e:
            messagebox.showerror("Database Error", str(e))
