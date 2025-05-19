import tkinter as tk

def tampilkan_dosen_view(root, id_user):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Selamat datang Dosen!").pack(pady=20)
    # Tambahkan lihat jadwal, edit/hapus, dll.
