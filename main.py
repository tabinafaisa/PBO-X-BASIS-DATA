import tkinter as tk
from views.login_view import LoginWindow
from views.mahasiswa_view import MahasiswaView
from utils.presensi_tools import insert_presensi_alpa
# from views.dosen_view import DosenView  # Jika kamu punya
from models.database import get_user_role_by_id  # Fungsi untuk cek role user

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Presensi Digital")
        self.show_login()

    def show_login(self):
        # Tampilkan login
        self.clear_window()
        LoginWindow(self.root, self.on_login_success)

    def on_login_success(self, id_user, role):

        if role == 'mahasiswa':
            self.show_mahasiswa_view(id_user)
        elif role == 'dosen':
            insert_presensi_alpa()
            self.show_dosen_view(id_user)
        else:
            print("Role tidak dikenali:", role)

    def show_mahasiswa_view(self, id_user):
        print("Menampilkan view mahasiswa")  
        self.clear_window()
        MahasiswaView(self.root, id_user)


    def show_dosen_view(self, id_user):
        self.clear_window()
        from views.dosen_view import tampilkan_dosen_view
        tampilkan_dosen_view(self.root, id_user)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

