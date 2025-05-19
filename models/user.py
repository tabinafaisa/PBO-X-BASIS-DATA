class User:
    def __init__(self, id_user, username, role):
        self.id_user = id_user
        self.username = username
        self.role = role

    def tampil_data_user(self):
        raise NotImplementedError("Subclass harus override method ini.")
