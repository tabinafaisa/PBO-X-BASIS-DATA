from user import User

class Mahasiswa(User):
    def __init__(self, id_user, username, nim, nama, prodi):
        super().__init__(id_user, username, "mahasiswa")
        self.__nim = nim
        self.nama = nama
        self.prodi = prodi

    def tampil_data_user(self):
        return f"Mahasiswa: {self.nama}, NIM: {self.__nim}, Prodi: {self.prodi}"

    def get_nim(self):
        return self.__nim
