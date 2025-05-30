import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from views.login_view import LoginWindow
from views.mahasiswa_view import MahasiswaView
from views.dosen_view import tampilkan_dosen_view  # Pastikan ini ada
from utils.presensi_tools import insert_presensi_alpa

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Presensi Digital")
        self.show_login()

    def show_login(self):
        self.clear_window()
        LoginWindow(self.root, self.on_login_success)

    def on_login_success(self, id_user, role):
        print(f"Login berhasil. ID: {id_user}, Role: {role}")

        if role == 'mahasiswa':
            self.show_mahasiswa_view(id_user)
        elif role == 'dosen':
            self.show_dosen_view(id_user)
            insert_presensi_alpa()
        else:
            print("❌ Role tidak dikenali:", role)

    def show_mahasiswa_view(self, id_user):
        self.clear_window()
        MahasiswaView(self.root, id_user)

    def show_dosen_view(self, id_user):
        self.clear_window()
        tampilkan_dosen_view(self.root, id_user)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = ttk.Window(themename="cosmo")  
    app = App(root)
    root.mainloop()
