import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, Label
from PIL import Image, ImageTk
from views.login_view import LoginWindow
from models.database import get_connection

def tampilkan_dosen_view(root, id_user):
    def setup_ui():
        for widget in root.winfo_children():
            widget.destroy()

        root.configure(background='#ffffff')

        # === Header ===
        header_frame = ttk.Frame(root, padding=10)
        header_frame.pack(fill=X)
        header_frame.configure(style="Header.TFrame")
        style = ttk.Style()
        style.configure("Header.TFrame", background="#ffffff")

        # Logo kiri
        logo_path = "assets/logo.png"
        try:
            logo_img = Image.open(logo_path).resize((40, 40))
            logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = ttk.Label(header_frame, image=logo_photo, style="Header.TLabel")
            logo_label.image = logo_photo
            logo_label.pack(side=LEFT, padx=(0, 10))
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat logo: {e}")

        ttk.Label(header_frame, text="Sistem Jadwal Mengajar", font=("Helvetica", 16, "bold"),
                background="#ffffff").pack(side=LEFT)

        # Profil kanan
        profile_frame = ttk.Frame(header_frame, style="Header.TFrame")
        profile_frame.pack(side=RIGHT)

        conn = get_connection()
        if conn is None:
            messagebox.showerror("Database Error", "Tidak dapat menghubungkan ke database.")
            return
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT Nama_Dosen FROM dosen WHERE id_user = %s", (id_user,))
            nama_dosen_row = cursor.fetchone()
            if not nama_dosen_row:
                messagebox.showerror("Error", "Data dosen tidak ditemukan.")
                conn.close()
                return
            nama_dosen = nama_dosen_row[0]
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            conn.close()
            return
        conn.close()

        profile_info_frame = ttk.Frame(profile_frame, style="Header.TFrame")
        profile_info_frame.pack(side=RIGHT)

        # Foto profil
        profil_path = "assets/profile.png"
        try:
            profil_img = Image.open(profil_path).resize((40, 40))
            profil_photo = ImageTk.PhotoImage(profil_img)
            profil_label = Label(profile_info_frame, image=profil_photo, bg="#ffffff")
            profil_label.image = profil_photo
            profil_label.pack(side=RIGHT, padx=5)
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat foto profil: {e}")

        # Nama dosen
        ttk.Label(profile_info_frame, text=nama_dosen, font=("Helvetica", 10, "bold"),
                background="#ffffff").pack(side=RIGHT, padx=5, anchor="e")

        # === Body ===
        frame = ttk.Frame(root, padding=10)
        frame.pack(fill=BOTH, expand=True)

        tree = build_treeview(frame)
        load_data(tree)

        action_frame = ttk.Frame(root, padding=10)
        action_frame.pack()

        build_action_buttons(action_frame, tree)

        # === Tombol Logout di kanan bawah ===
        logout_frame = ttk.Frame(root)
        logout_frame.pack(fill=BOTH, expand=False, anchor=SE, padx=10, pady=10)

        def logout():
            try:
                # Clear all widgets to reset UI
                for widget in root.winfo_children():
                    widget.destroy()
                # Reinitialize login window
                LoginWindow(root, None)
            except Exception as e:
                messagebox.showerror("Error", f"Logout failed: {str(e)}")

        logout_btn = ttk.Button(logout_frame, text="Logout", bootstyle="danger", command=logout)
        logout_btn.pack(anchor=SE)

    def build_treeview(parent):
        columns = ("nama_mk", "kelas", "pertemuan", "tanggal", "jam")
        tree = ttk.Treeview(parent, columns=columns, show="headings", bootstyle="info")
        for col in columns:
            tree.heading(col, text=col.replace("_", " ").title())
        tree.pack(fill=BOTH, expand=True)
        return tree

    def build_action_buttons(parent, tree):
        ttk.Button(parent, text="\U0001F441 Lihat Presensi",
                   command=lambda: lihat_presensi_by_pertemuan(tree.selection()[0]) if tree.selection() else messagebox.showwarning("Pilih Pertemuan", "Pilih dulu satu pertemuan."),
                   bootstyle="info").grid(row=0, column=0, padx=5)

        ttk.Button(parent, text="\U0001F552 Edit Jam",
                   command=lambda: tampilkan_edit_jam_window(tree.selection()[0]) if tree.selection() else messagebox.showwarning("Pilih Pertemuan", "Pilih dulu satu pertemuan."),
                   bootstyle="warning").grid(row=0, column=1, padx=5)

        ttk.Button(parent, text="❌ Hapus Pertemuan",
                   command=lambda: batal_pertemuan(tree),
                   bootstyle="danger").grid(row=0, column=2, padx=5)

        ttk.Button(parent, text="➕ Tambah Pertemuan",
                   command=tampilkan_tambah_pertemuan_window,
                   bootstyle="success").grid(row=0, column=3, padx=5)

    def load_data(tree):
        conn = get_connection()
        if conn is None:
            messagebox.showerror("Database Error", "Tidak dapat menghubungkan ke database.")
            return
        try:
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
            rows = cursor.fetchall()
            tree.delete(*tree.get_children())
            for row in rows:
                id_pertemuan, nama_mk, kelas, pertemuan_ke, tanggal, jam_mulai, jam_selesai = row
                jam = f"{jam_mulai} - {jam_selesai}"
                tree.insert("", "end", iid=str(id_pertemuan), values=(nama_mk, kelas, pertemuan_ke, tanggal, jam))
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()

    def lihat_presensi_by_pertemuan(id_pertemuan):
        window = ttk.Toplevel(root)
        window.title("Presensi Mahasiswa per Pertemuan")
        window.geometry("600x400")

        conn = get_connection()
        if conn is None:
            messagebox.showerror("Database Error", "Tidak dapat menghubungkan ke database.")
            window.destroy()
            return

        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT mk.Nama_MK, k.Keterangan
                FROM pertemuan per
                JOIN matakuliah mk ON per.Kode_MK = mk.Kode_MK
                JOIN kelas k ON per.Kode_Kelas = k.Kode_Kelas
                WHERE per.ID_Pertemuan = %s
            """, (id_pertemuan,))
            result = cursor.fetchone()
            if result:
                nama_mk, keterangan_kelas = result
            else:
                messagebox.showerror("Error", "Data pertemuan tidak ditemukan.")
                window.destroy()
                return

            ttk.Label(window, text=f"Kelas {keterangan_kelas} - {nama_mk}", font=("Helvetica", 14, "bold")).pack(anchor="w", padx=10, pady=10)

            # === Hanya NIM, Nama, dan Status ===
            tree = ttk.Treeview(window, columns=("nim", "nama", "status"), show="headings", bootstyle="info")
            for col in ("nim", "nama", "status"):
                tree.heading(col, text=col.title())
            tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

            cursor.execute("""
                SELECT m.NIM, m.Nama, s.Keterangan
                FROM presensi p
                JOIN mahasiswa m ON p.NIM = m.NIM
                JOIN status_presensi s ON p.Kode_Status = s.Kode_Status
                WHERE p.ID_Pertemuan = %s
            """, (id_pertemuan,))
            for row in cursor.fetchall():
                tree.insert("", "end", values=row)

        except Exception as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            conn.close()

        ttk.Button(window, text="Kembali", command=window.destroy, bootstyle="secondary").pack(pady=10)

    def tampilkan_edit_jam_window(id_pertemuan):
        window = ttk.Toplevel(root)
        window.title("Edit Jam Pertemuan")
        window.geometry("300x200")

        ttk.Label(window, text="Jam Mulai (HH:MM:SS)").pack(pady=5)
        entry_mulai = ttk.Entry(window)
        entry_mulai.pack()

        ttk.Label(window, text="Jam Selesai (HH:MM:SS)").pack(pady=5)
        entry_selesai = ttk.Entry(window)
        entry_selesai.pack()

        conn = get_connection()
        if conn is None:
            messagebox.showerror("Database Error", "Tidak dapat menghubungkan ke database.")
            window.destroy()
            return

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT Jam_mulai, Jam_selesai FROM pertemuan WHERE ID_Pertemuan = %s", (id_pertemuan,))
            result = cursor.fetchone()
            if result:
                jam_mulai, jam_selesai = result
            else:
                messagebox.showerror("Error", "Data pertemuan tidak ditemukan.")
                window.destroy()
                return
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            window.destroy()
            return
        finally:
            conn.close()

        entry_mulai.insert(0, str(jam_mulai))
        entry_selesai.insert(0, str(jam_selesai))

        def simpan_perubahan():
            try:
                conn = get_connection()
                if conn is None:
                    messagebox.showerror("Database Error", "Tidak dapat menghubungkan ke database.")
                    return
                cursor = conn.cursor()
                cursor.execute("UPDATE pertemuan SET Jam_mulai = %s, Jam_selesai = %s WHERE ID_Pertemuan = %s",
                               (entry_mulai.get(), entry_selesai.get(), id_pertemuan))
                conn.commit()
                messagebox.showinfo("Berhasil", "Jam berhasil diperbarui.")
                window.destroy()
                tampilkan_dosen_view(root, id_user)
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                if conn:
                    conn.close()

        ttk.Button(window, text="Simpan", command=simpan_perubahan, bootstyle="success").pack(pady=10)

    def tampilkan_tambah_pertemuan_window():
        window = ttk.Toplevel(root)
        window.title("Tambah Pertemuan")
        window.geometry("400x400")

        ttk.Label(window, text="Mata Kuliah").pack()
        mk_combo = ttk.Combobox(window)
        mk_combo.pack()

        ttk.Label(window, text="Kelas").pack()
        kelas_combo = ttk.Combobox(window)
        kelas_combo.pack()

        ttk.Label(window, text="Tanggal (YYYY-MM-DD)").pack()
        entry_tanggal = ttk.Entry(window)
        entry_tanggal.pack()

        ttk.Label(window, text="Pertemuan Ke").pack()
        entry_pertemuan = ttk.Entry(window)
        entry_pertemuan.pack()

        ttk.Label(window, text="Jam Mulai (HH:MM:SS)").pack()
        entry_mulai = ttk.Entry(window)
        entry_mulai.pack()

        ttk.Label(window, text="Jam Selesai (HH:MM:SS)").pack()
        entry_selesai = ttk.Entry(window)
        entry_selesai.pack()

        conn = get_connection()
        if conn is None:
            messagebox.showerror("Database Error", "Tidak dapat menghubungkan ke database.")
            window.destroy()
            return

        try:
            cursor = conn.cursor()
            cursor.execute("SELECT Kode_MK, Nama_MK FROM matakuliah")
            mk_combo["values"] = [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]
            cursor.execute("SELECT Kode_Kelas, Keterangan FROM kelas")
            kelas_combo["values"] = [f"{row[0]} - {row[1]}" for row in cursor.fetchall()]
            cursor.execute("SELECT Kode_Dosen FROM dosen WHERE id_user = %s", (id_user,))
            kode_dosen_row = cursor.fetchone()
            if not kode_dosen_row:
                messagebox.showerror("Error", "Data dosen tidak ditemukan.")
                window.destroy()
                return
            kode_dosen = kode_dosen_row[0]
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            window.destroy()
            return
        finally:
            conn.close()

        def simpan():
            try:
                conn = get_connection()
                if conn is None:
                    messagebox.showerror("Database Error", "Tidak dapat menghubungkan ke database.")
                    return
                cursor = conn.cursor()
                kode_mk = mk_combo.get().split(" - ")[0]
                kode_kelas = kelas_combo.get().split(" - ")[0]
                cursor.execute("""
                    INSERT INTO pertemuan (Kode_MK, Kode_Dosen, Kode_Kelas, Tanggal, Pertemuan_ke, Jam_mulai, Jam_selesai)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    kode_mk, kode_dosen, kode_kelas,
                    entry_tanggal.get(), int(entry_pertemuan.get()),
                    entry_mulai.get(), entry_selesai.get()
                ))
                conn.commit()
                messagebox.showinfo("Sukses", "Pertemuan berhasil ditambahkan.")
                window.destroy()
                tampilkan_dosen_view(root, id_user)
            except Exception as e:
                messagebox.showerror("Error", str(e))
            finally:
                if conn:
                    conn.close()

        ttk.Button(window, text="Simpan", command=simpan, bootstyle="primary").pack(pady=10)

    def batal_pertemuan(tree):
        selected = tree.selection()
        if selected:
            id_pertemuan = selected[0]
            if messagebox.askyesno("Konfirmasi", "Yakin ingin membatalkan pertemuan ini?"):
                try:
                    conn = get_connection()
                    if conn is None:
                        messagebox.showerror("Database Error", "Tidak dapat menghubungkan ke database.")
                        return
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM presensi WHERE ID_Pertemuan = %s", (id_pertemuan,))
                    cursor.execute("DELETE FROM pertemuan WHERE ID_Pertemuan = %s", (id_pertemuan,))
                    conn.commit()
                    messagebox.showinfo("Berhasil", "Pertemuan berhasil dibatalkan.")
                    tampilkan_dosen_view(root, id_user)
                except Exception as e:
                    messagebox.showerror("Error", str(e))
                finally:
                    if conn:
                        conn.close()

    setup_ui()

