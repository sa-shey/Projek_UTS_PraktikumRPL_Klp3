import mysql.connector
from config.database import Database


class TransaksiModel:
    def __init__(self):
        self.db = Database()
        self.table_name = "transaksi_laundry"

    def get_all_transaksi(self):
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                query = f"""
                    SELECT t.*, p.nama AS nama_pelanggan, pk.nama_paket 
                    FROM {self.table_name} t
                    JOIN pelanggan p ON t.id_pelanggan = p.id_pelanggan
                    JOIN paket_layanan pk ON t.id_paket = pk.id_paket
                    ORDER BY t.id_transaksi ASC
                """
                cursor.execute(query)
                result = cursor.fetchall()
                cursor.close()
                conn.close()
                return result
            except mysql.connector.Error as e:
                print(f"Error Read Transaksi: {e}")
                conn.close()
                return []
        return []

    def create_transaksi(
        self,
        id_pelanggan,
        id_paket,
        berat_kg,
        tgl_terima,
        tgl_selesai,
        total_biaya,
        status_cucian,
    ):
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = f"""
                    INSERT INTO {self.table_name} 
                    (id_pelanggan, id_paket, berat_kg, tgl_terima, tgl_selesai, total_biaya, status_cucian) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                val = (
                    id_pelanggan,
                    id_paket,
                    berat_kg,
                    tgl_terima,
                    tgl_selesai if tgl_selesai else None,
                    total_biaya,
                    status_cucian,
                )
                cursor.execute(query, val)
                conn.commit()
                cursor.close()
                conn.close()
                return True
            except mysql.connector.Error as e:
                conn.rollback()
                print(f"Error Create Transaksi: {e}")
                conn.close()
                return False
        return False

    def update_transaksi(
        self,
        id_transaksi,
        id_pelanggan,
        id_paket,
        berat_kg,
        tgl_terima,
        tgl_selesai,
        total_biaya,
        status_cucian,
    ):
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = f"""
                    UPDATE {self.table_name}
                    SET id_pelanggan = %s,
                        id_paket = %s,
                        berat_kg = %s,
                        tgl_terima = %s,
                        tgl_selesai = %s,
                        total_biaya = %s,
                        status_cucian = %s
                    WHERE id_transaksi = %s
                """
                val = (
                    id_pelanggan,
                    id_paket,
                    berat_kg,
                    tgl_terima,
                    tgl_selesai if tgl_selesai else None,
                    total_biaya,
                    status_cucian,
                    id_transaksi,
                )
                cursor.execute(query, val)
                conn.commit()
                berhasil = cursor.rowcount >= 0
                cursor.close()
                conn.close()
                return berhasil
            except mysql.connector.Error as e:
                conn.rollback()
                print(f"Error Update Transaksi: {e}")
                conn.close()
                return False
        return False

    def update_status(self, id_transaksi, status_cucian):
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = f"UPDATE {self.table_name} SET status_cucian = %s WHERE id_transaksi = %s"
                val = (status_cucian, id_transaksi)
                cursor.execute(query, val)
                conn.commit()
                cursor.close()
                conn.close()
                return True
            except mysql.connector.Error as e:
                conn.rollback()
                print(f"Error Update Status Transaksi: {e}")
                conn.close()
                return False
        return False

    def delete_transaksi(self, id_transaksi):
        conn = self.db.get_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = f"DELETE FROM {self.table_name} WHERE id_transaksi = %s"
                cursor.execute(query, (id_transaksi,))
                conn.commit()
                terhapus = cursor.rowcount > 0
                cursor.close()
                conn.close()
                return terhapus
            except mysql.connector.Error as e:
                conn.rollback()
                print(f"Error Delete Transaksi: {e}")
                conn.close()
                return False
        return False