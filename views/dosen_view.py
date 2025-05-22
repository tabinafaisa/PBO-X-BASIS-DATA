# import tkinter as tk

# def tampilkan_dosen_view(root, id_user):
#     for widget in root.winfo_children():
#         widget.destroy()

#     tk.Label(root, text="Selamat datang Dosen!").pack(pady=20)
#     # Tambahkan lihat jadwal, edit/hapus, dll.

# from tkinter import messagebox

# def lihat_presensi():
#     messagebox.showinfo("Lihat Presensi", "Fitur lihat presensi belum diimplementasikan.")

# def lihat_jadwal():
#     messagebox.showinfo("Lihat Jadwal", "Fitur lihat jadwal belum diimplementasikan.")

# def edit_data():
#     messagebox.showinfo("Edit Data", "Fitur edit data belum diimplementasikan.")

# def hapus_data():
#     messagebox.showinfo("Hapus Data", "Fitur hapus data belum diimplementasikan.")

# def tampilkan_dosen_view(root, id_user):
#     for widget in root.winfo_children():
#         widget.destroy()

#     tk.Label(root, text="Selamat datang Dosen!", font=("Arial", 16)).pack(pady=20)

#     btn_presensi = tk.Button(root, text="Lihat Presensi", width=20, command=lihat_presensi)
#     btn_presensi.pack(pady=5)

#     btn_jadwal = tk.Button(root, text="Lihat Jadwal", width=20, command=lihat_jadwal)
#     btn_jadwal.pack(pady=5)

#     btn_edit = tk.Button(root, text="Edit Data", width=20, command=edit_data)
#     btn_edit.pack(pady=5)

#     btn_hapus = tk.Button(root, text="Hapus Data", width=20, command=hapus_data)
#     btn_hapus.pack(pady=5)
import tkinter as tk
from tkinter import ttk, messagebox
from utils.db import get_connection

def tampilkan_lihat_presensi(id_user):
    from utils.db import get_connection

    window = tk.Toplevel()
    window.title("Rekap Presensi Mahasiswa")
    window.geometry("1000x500")

    tk.Label(window, text="Rekap Presensi Mahasiswa", font=("Arial", 14)).pack(pady=10)

    columns = ("nim", "nama", "matkul", "pertemuan", "tanggal", "jam", "status")
    tree = ttk.Treeview(window, columns=columns, show="headings")
    tree.heading("nim", text="NIM")
    tree.heading("nama", text="Nama")
    tree.heading("matkul", text="Mata Kuliah")
    tree.heading("pertemuan", text="Pertemuan Ke")
    tree.heading("tanggal", text="Tanggal")
    tree.heading("jam", text="Jam")
    tree.heading("status", text="Status")
    tree.pack(fill=tk.BOTH, expand=True)

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc('get_rekap_presensi_dosen', [id_user])
        for result in cursor.stored_results():
            for row in result.fetchall():
                jam = f"{row[6]} - {row[7]}"
                tree.insert("", tk.END, values=(row[0], row[1], row[2], row[5], row[5], jam, row[9]))
    except Exception as e:
        messagebox.showerror("Gagal", f"Gagal mengambil data presensi.\n{str(e)}")
    finally:
        conn.close()

def tampilkan_edit_jam_window(id_pertemuan, id_user, parent_root):
    window = tk.Toplevel()
    window.title("Edit Jam Pertemuan")
    window.geometry("300x150")

    tk.Label(window, text="Jam Mulai (HH:MM:SS)").pack(pady=5)
    entry_mulai = tk.Entry(window)
    entry_mulai.pack()

    tk.Label(window, text="Jam Selesai (HH:MM:SS)").pack(pady=5)
    entry_selesai = tk.Entry(window)
    entry_selesai.pack()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Jam_mulai, Jam_selesai FROM pertemuan WHERE ID_Pertemuan = %s", (id_pertemuan,))
    jam_mulai, jam_selesai = cursor.fetchone()
    conn.close()

    entry_mulai.insert(0, str(jam_mulai))
    entry_selesai.insert(0, str(jam_selesai))

    def simpan_perubahan():
        new_mulai = entry_mulai.get()
        new_selesai = entry_selesai.get()
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE pertemuan SET Jam_mulai = %s, Jam_selesai = %s WHERE ID_Pertemuan = %s",
                           (new_mulai, new_selesai, id_pertemuan))
            conn.commit()
            conn.close()
            messagebox.showinfo("Berhasil", "Jam berhasil diperbarui.")
            window.destroy()
            tampilkan_dosen_view(parent_root, id_user)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(window, text="Simpan", command=simpan_perubahan).pack(pady=10)

def lihat_presensi_by_pertemuan(id_pertemuan):
    window = tk.Toplevel()
    window.title("Presensi Mahasiswa")
    window.geometry("800x400")

    tree = ttk.Treeview(window, columns=("nim", "nama", "status"), show="headings")
    tree.heading("nim", text="NIM")
    tree.heading("nama", text="Nama")
    tree.heading("status", text="Status")
    tree.pack(fill=tk.BOTH, expand=True)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.NIM, m.Nama, s.Keterangan
        FROM presensi p
        JOIN mahasiswa m ON p.NIM = m.NIM
        JOIN status_presensi s ON p.Kode_Status = s.Kode_Status
        WHERE p.ID_Pertemuan = %s
    """, (id_pertemuan,))
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)
    conn.close()

def tampilkan_dosen_view(root, id_user):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Jadwal Mengajar Anda", font=("Arial", 16)).pack(pady=10)

    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    # Tampilkan hanya 4 kolom
    columns = ("nama_mk", "pertemuan", "jam_mulai", "jam_selesai")
    tree = ttk.Treeview(frame, columns=columns, show="headings")
    tree.heading("nama_mk", text="Mata Kuliah")
    tree.heading("pertemuan", text="Pertemuan Ke")
    tree.heading("jam_mulai", text="Jam Mulai")
    tree.heading("jam_selesai", text="Jam Selesai")
    tree.pack(fill=tk.BOTH, expand=True)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT per.ID_Pertemuan, mk.Nama_MK, per.Pertemuan_ke, per.Jam_mulai, per.Jam_selesai
        FROM pertemuan per
        JOIN matakuliah mk ON per.Kode_MK = mk.Kode_MK
        JOIN dosen d ON per.Kode_Dosen = d.Kode_Dosen
        WHERE d.id_user = %s
    """, (id_user,))
    data = cursor.fetchall()
    conn.close()

    for row in data:
        id_pertemuan = row[0]
        display_data = row[1:]  # hanya: nama_mk, pertemuan_ke, jam_mulai, jam_selesai
        tree.insert("", tk.END, iid=str(id_pertemuan), values=display_data)
    

    def buka_presensi():
        selected = tree.selection()
        if selected:
            id_pertemuan = selected[0]
            lihat_presensi_by_pertemuan(id_pertemuan)

    def buka_edit_jam():
        selected = tree.selection()
        if selected:
            id_pertemuan = selected[0]
            tampilkan_edit_jam_window(id_pertemuan, id_user, root)

    def batal_pertemuan():
        selected = tree.selection()
        if selected:
            id_pertemuan = selected[0]
            if messagebox.askyesno("Konfirmasi", "Yakin ingin membatalkan pertemuan ini?"):
                conn = get_connection()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM presensi WHERE ID_Pertemuan = %s", (id_pertemuan,))
                cursor.execute("DELETE FROM pertemuan WHERE ID_Pertemuan = %s", (id_pertemuan,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Berhasil", "Pertemuan dibatalkan.")
                tampilkan_dosen_view(root, id_user)

    action_frame = tk.Frame(root)
    action_frame.pack(pady=10)

    tk.Button(action_frame, text="Lihat Presensi Keseluruhan", command=lambda: tampilkan_lihat_presensi(id_user)).grid(row=0, column=0, padx=5)
    tk.Button(action_frame, text="Edit Jam", command=buka_edit_jam).grid(row=0, column=1, padx=5)
    tk.Button(action_frame, text="Batal Pertemuan", command=batal_pertemuan, bg="red", fg="white").grid(row=0, column=2, padx=5)
