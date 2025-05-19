import tkinter as tk

def tampilkan_mahasiswa_view(root, id_user):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Selamat datang Mahasiswa!").pack(pady=20)
    # Tambahkan tombol presensi, rekap, dll.
