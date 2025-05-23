import tkinter as tk
from tkinter import ttk, messagebox
from models.database import get_connection

def tampilkan_dosen_view(root, id_user):
    def lihat_presensi_by_pertemuan(id_pertemuan):
        window = tk.Toplevel(root)
        window.title("Presensi Mahasiswa per Pertemuan")
        window.geometry("1000x500")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT mk.Nama_MK, k.Keterangan
            FROM pertemuan per
            JOIN matakuliah mk ON per.Kode_MK = mk.Kode_MK
            JOIN kelas k ON per.Kode_Kelas = k.Kode_Kelas
            WHERE per.ID_Pertemuan = %s
        """, (id_pertemuan,))
        nama_mk, keterangan_kelas = cursor.fetchone()

        tk.Label(window, text=f"Kelas {keterangan_kelas} - {nama_mk}", font=("Arial", 12, "bold"), anchor="w").pack(anchor="w", padx=10, pady=5)

        tree = ttk.Treeview(window, columns=("nim", "nama", "matkul", "pertemuan", "jam", "status"), show="headings")
        tree.heading("nim", text="NIM")
        tree.heading("nama", text="Nama")
        tree.heading("matkul", text="Mata Kuliah")
        tree.heading("pertemuan", text="Pertemuan")
        tree.heading("jam", text="Jam")
        tree.heading("status", text="Status")
        tree.pack(fill=tk.BOTH, expand=True)

        cursor.execute("""
            SELECT m.NIM, m.Nama, mk.Nama_MK, per.Pertemuan_ke,
                   CONCAT(per.Jam_mulai, ' - ', per.Jam_selesai), s.Keterangan
            FROM presensi p
            JOIN mahasiswa m ON p.NIM = m.NIM
            JOIN pertemuan per ON p.ID_Pertemuan = per.ID_Pertemuan
            JOIN matakuliah mk ON per.Kode_MK = mk.Kode_MK
            JOIN status_presensi s ON p.Kode_Status = s.Kode_Status
            WHERE p.ID_Pertemuan = %s
        """, (id_pertemuan,))
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)

        conn.close()

        tk.Button(window, text="Kembali", command=window.destroy, bg="gray", fg="white").pack(pady=10)

    def tampilkan_edit_jam_window(id_pertemuan):
        window = tk.Toplevel(root)
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
                tampilkan_dosen_view(root, id_user)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(window, text="Simpan", command=simpan_perubahan).pack(pady=10)

    def tampilkan_tambah_pertemuan_window():
        window = tk.Toplevel(root)
        window.title("Tambah Pertemuan")
        window.geometry("400x400")

        tk.Label(window, text="Mata Kuliah").pack()
        mk_combo = ttk.Combobox(window)
        mk_combo.pack()

        tk.Label(window, text="Kelas").pack()
        kelas_combo = ttk.Combobox(window)
        kelas_combo.pack()

        tk.Label(window, text="Tanggal (YYYY-MM-DD)").pack()
        entry_tanggal = tk.Entry(window)
        entry_tanggal.pack()

        tk.Label(window, text="Pertemuan Ke").pack()
        entry_pertemuan = tk.Entry(window)
        entry_pertemuan.pack()

        tk.Label(window, text="Jam Mulai (HH:MM:SS)").pack()
        entry_mulai = tk.Entry(window)
        entry_mulai.pack()

        tk.Label(window, text="Jam Selesai (HH:MM:SS)").pack()
        entry_selesai = tk.Entry(window)
        entry_selesai.pack()

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Kode_MK, Nama_MK FROM matakuliah")
        mk_combo["values"] = [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]

        cursor.execute("SELECT Kode_Kelas, Keterangan FROM kelas")
        kelas_combo["values"] = [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]

        cursor.execute("SELECT Kode_Dosen FROM dosen WHERE id_user = %s", (id_user,))
        kode_dosen = cursor.fetchone()[0]

        def simpan():
            try:
                kode_mk = mk_combo.get().split(" - ")[0]
                kode_kelas = kelas_combo.get().split(" - ")[0]
                tanggal = entry_tanggal.get()
                pertemuan_ke = int(entry_pertemuan.get())
                jam_mulai = entry_mulai.get()
                jam_selesai = entry_selesai.get()

                cursor.execute("""
                    INSERT INTO pertemuan (Kode_MK, Kode_Dosen, Kode_Kelas, Tanggal, Pertemuan_ke, Jam_mulai, Jam_selesai)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (kode_mk, kode_dosen, kode_kelas, tanggal, pertemuan_ke, jam_mulai, jam_selesai))
                conn.commit()
                messagebox.showinfo("Sukses", "Pertemuan berhasil ditambahkan.")
                window.destroy()
                tampilkan_dosen_view(root, id_user)
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                conn.close()

        tk.Button(window, text="Simpan", command=simpan).pack(pady=10)

    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Jadwal Mengajar Anda", font=("Arial", 16)).pack(pady=10)

    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)

    columns = ("nama_mk", "kelas", "pertemuan", "tanggal", "jam")
    tree = ttk.Treeview(frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col.replace("_", " ").title())
    tree.pack(fill=tk.BOTH, expand=True)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT per.ID_Pertemuan, mk.Nama_MK, k.Keterangan, per.Pertemuan_ke,
               per.Tanggal, per.Jam_mulai, per.Jam_selesai
        FROM pertemuan per
        JOIN matakuliah mk ON per.Kode_MK = mk.Kode_MK
        JOIN kelas k ON per.Kode_Kelas = k.Kode_Kelas
        JOIN dosen d ON per.Kode_Dosen = d.Kode_Dosen
        WHERE d.id_user = %s
        ORDER BY per.Tanggal
    """, (id_user,))
    for row in cursor.fetchall():
        id_pertemuan, nama_mk, kelas, pertemuan_ke, tanggal, jam_mulai, jam_selesai = row
        jam = f"{jam_mulai} - {jam_selesai}"
        tree.insert("", tk.END, iid=str(id_pertemuan), values=(nama_mk, kelas, pertemuan_ke, tanggal, jam))

    conn.close()

    def buka_edit_jam():
        selected = tree.selection()
        if selected:
            tampilkan_edit_jam_window(selected[0])

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

    tk.Button(action_frame, text="Lihat Presensi per Pertemuan", command=lambda: lihat_presensi_by_pertemuan(tree.selection()[0]) if tree.selection() else messagebox.showwarning("Pilih Pertemuan", "Silakan pilih satu pertemuan dulu.")).grid(row=0, column=0, padx=5)
    tk.Button(action_frame, text="Edit Jam", command=buka_edit_jam).grid(row=0, column=1, padx=5)
    tk.Button(action_frame, text="Batal Pertemuan", command=batal_pertemuan, bg="red", fg="white").grid(row=0, column=2, padx=5)
    tk.Button(action_frame, text="Tambah Pertemuan", command=tampilkan_tambah_pertemuan_window, bg="green", fg="white").grid(row=0, column=3, padx=5)