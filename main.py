# import tkinter as tk
# from views.login_view import LoginWindow  # ✅ Import class, bukan fungsi

# def main():
#     root = tk.Tk()
#     app = LoginWindow(root)  # ✅ Instansiasi class LoginWindow
#     root.mainloop()

# if __name__ == "__main__":
# #     main()
# from tkinter import Tk
# from views.mahasiswa_view import MahasiswaView

# if __name__ == "__main__":
#     root = Tk()
#     id_user = 2  # Ganti dengan id_user hasil login
#     app = MahasiswaView(root, id_user)
#     root.mainloop()
import tkinter as tk
from views.login_view import LoginWindow
from views.mahasiswa_view import MahasiswaView
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
        # Panggil ketika login berhasil
        # role = get_user_role_by_id(id_user)

        if role == 'mahasiswa':
            self.show_mahasiswa_view(id_user)
        elif role == 'dosen':
            self.show_dosen_view(id_user)
        else:
            print("Role tidak dikenali:", role)

    def show_mahasiswa_view(self, id_user):
        print("Menampilkan view mahasiswa")  # ⬅ Tambahkan
        self.clear_window()
        MahasiswaView(self.root, id_user)


    # def show_dosen_view(self, id_user):
    #     self.clear_window()
    #     DosenView(self.root, id_user)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()

