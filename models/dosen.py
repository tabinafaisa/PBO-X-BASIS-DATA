from .user import User

class Dosen(User):
    def __init__(self, id_user, username, kode_dosen, nama_dosen):
        super().__init__(id_user, username, "dosen")
        self.kode_dosen = kode_dosen
        self.nama_dosen = nama_dosen

    def tampil_data_user(self):
        return f"Dosen: {self.nama_dosen}, Kode: {self.kode_dosen}"
