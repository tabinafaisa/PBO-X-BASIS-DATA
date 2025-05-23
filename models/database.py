import mysql.connector
from datetime import datetime
from utils.db import get_connection

def get_jadwal_mahasiswa_hari_ini(id_user):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="tugas_akhir"
    )
    cursor = conn.cursor(dictionary=True)

    query = """
    SELECT DISTINCT
        p.ID_Pertemuan,
        mk.Nama_MK,
        d.Nama_Dosen,
        k.Keterangan AS Nama_Kelas,
        p.Tanggal,
        p.Pertemuan_ke,
        p.Jam_mulai,
        p.Jam_selesai,
        pr.Waktu_presensi,
        sp.Keterangan AS Status,
        m.NIM  -- Diperlukan untuk input presensi
    FROM mahasiswa m
    JOIN users u ON m.Id_user = u.ID_User
    JOIN kelas_mahasiswa km ON m.NIM = km.NIM
    JOIN pertemuan p ON p.Kode_Kelas = km.Kode_Kelas
    JOIN matakuliah mk ON mk.Kode_MK = p.Kode_MK
    JOIN dosen d ON d.Kode_Dosen = p.Kode_Dosen
    JOIN kelas k ON k.Kode_Kelas = p.Kode_Kelas
    LEFT JOIN presensi pr ON pr.ID_Pertemuan = p.ID_Pertemuan AND pr.NIM = m.NIM
    LEFT JOIN status_presensi sp ON pr.Kode_Status = sp.Kode_Status
    WHERE u.ID_User = %s AND DATE(p.Tanggal) = CURDATE()
    """
    cursor.execute(query, (id_user,))
    result = cursor.fetchall()
    print("Jadwal ditemukan:", result)
    cursor.close()
    conn.close()
    return result


def get_user_role_by_id(id_user):
    db = get_connection()
    cursor = db.cursor()
    query = "SELECT role FROM users WHERE id_user = %s"
    cursor.execute(query, (id_user,))
    result = cursor.fetchone()
    if result:
        return result[0]
    return None

def insert_presensi(nim, id_pertemuan):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="tugas_akhir"
    )
    cursor = conn.cursor()
    
    now = datetime.now().strftime('%H:%M:%S')
    kode_status = 'H'  # Hadir

    # Cek apakah sudah presensi
    cursor.execute("SELECT * FROM presensi WHERE NIM = %s AND ID_Pertemuan = %s", (nim, id_pertemuan))
    existing = cursor.fetchone()
    if not existing:
        cursor.execute("""
            INSERT INTO presensi (ID_Pertemuan, NIM, Waktu_presensi, Kode_Status)
            VALUES (%s, %s, %s, %s)
        """, (id_pertemuan, nim, now, kode_status))
        conn.commit()
    
    cursor.close()
    conn.close()

