import tkinter as tk
from tkinter import messagebox
from utils.hashing import hash_password
from db import get_connection
from views.mahasiswa_view import tampilkan_mahasiswa_view
from views.dosen_view import tampilkan_dosen_view

def tampilkan_login(root):
    frame = tk.Frame(root)
    frame.pack(pady=30)

    tk.Label(frame, text="Username").grid(row=0, column=0)
    username_entry = tk.Entry(frame)
    username_entry.grid(row=0, column=1)

    tk.Label(frame, text="Password").grid(row=1, column=0)
    password_entry = tk.Entry(frame, show="*")
    password_entry.grid(row=1, column=1)

    def proses_login():
        conn = get_connection()
        cursor = conn.cursor()
        username = username_entry.get()
        password = hash_password(password_entry.get())

        cursor.execute("SELECT ID_User, role FROM users WHERE username=%s AND password=%s", (username, password))
        result = cursor.fetchone()
        conn.close()

        if result:
            id_user, role = result
            if role == "mahasiswa":
                tampilkan_mahasiswa_view(root, id_user)
            else:
                tampilkan_dosen_view(root, id_user)
        else:
            messagebox.showerror("Login Gagal", "Username atau password salah.")

    tk.Button(frame, text="Login", command=proses_login).grid(columnspan=2, pady=10)
