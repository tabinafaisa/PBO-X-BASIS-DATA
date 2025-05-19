from db import get_connection

class Presensi:
    @staticmethod
    def create_presensi(nim, id_pertemuan, waktu_presensi, kode_status):
        conn = get_connection()
        cursor = conn.cursor()
        query = "INSERT INTO presensi (NIM, ID_Pertemuan, Waktu_presensi, Kode_Status) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (nim, id_pertemuan, waktu_presensi, kode_status))
        conn.commit()
        conn.close()
