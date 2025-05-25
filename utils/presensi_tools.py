from utils.db import get_connection
from datetime import date, datetime

def insert_presensi_alpa():
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO presensi (NIM, ID_Pertemuan)
        SELECT km.NIM, p.ID_Pertemuan
        FROM pertemuan p
        JOIN kelas_mahasiswa km ON km.Kode_Kelas = p.Kode_Kelas
        WHERE p.Tanggal = CURDATE()
          AND CURRENT_TIME() > p.Jam_selesai
          AND NOT EXISTS (
              SELECT 1 FROM presensi pr
              WHERE pr.NIM = km.NIM AND pr.ID_Pertemuan = p.ID_Pertemuan
          );
    """

    try:
        cursor.execute(query)
        conn.commit()
        print("✅ Alpa inserted successfully.")
    except Exception as e:
        print("❌ Gagal insert alpa:", e)

    conn.close()
