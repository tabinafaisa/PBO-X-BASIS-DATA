import tkinter as tk
from views.login_view import tampilkan_login

root = tk.Tk()
root.title("Aplikasi Presensi Digital")
root.geometry("400x300")

tampilkan_login(root)

root.mainloop()
