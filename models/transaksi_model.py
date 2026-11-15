
import mysql.connector
from config.database import Database


class TransaksiModel:
    def __init__(self):
        self.db = Database()
        self.table_name = "transaksi_laundry"

    def _get_conn(self):
        return self.db.get_connection()

    # READ: Menampilkan semua transaksi untuk kasir dan manajer
    def get_all_transaksi(self):
        conn = self._get_conn()
        cursor = None
        if not conn:
            return []

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
            return result
        except mysql.connector.Error as e:
            print(f"Error Read Transaksi: {e}")
            return []
        finally:
            if cursor is not None:
                cursor.close()
            conn.close()

    # READ: Menampilkan transaksi milik pelanggan yang sedang login
    def get_transaksi_by_user(self, id_user):
        conn = self._get_conn()
        cursor = None

        if not conn:
            return []

        try:
            cursor = conn.cursor(dictionary=True)

            query = """
                SELECT
                    t.id_transaksi,
                    t.tgl_terima,
                    t.tgl_selesai,
                    t.berat_kg,
                    t.total_biaya,
                    t.status_cucian,
                    pk.nama_paket
                FROM transaksi_laundry t
                JOIN pelanggan p
                    ON t.id_pelanggan = p.id_pelanggan
                JOIN paket_layanan pk
                    ON t.id_paket = pk.id_paket
                WHERE p.id_user = %s
                ORDER BY t.id_transaksi DESC
            """

            cursor.execute(query, (id_user,))
            return cursor.fetchall()

        except mysql.connector.Error as e:
            print(f"Error transaksi pelanggan: {e}")
            return []

        finally:
            if cursor is not None:
                cursor.close()
            conn.close()

    # READ: Menampilkan transaksi berdasarkan ID
    def get_transaksi_by_id(self, id_transaksi):
        conn = self._get_conn()
        cursor = None
        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            query = f"SELECT * FROM {self.table_name} WHERE id_transaksi = %s"
            cursor.execute(query, (id_transaksi,))
            return cursor.fetchone()
        except mysql.connector.Error as e:
            print(f"Error Read Transaksi By ID: {e}")
            return None
        finally:
            if cursor is not None:
                cursor.close()
            conn.close()

    # CREATE: Menambahkan transaksi baru
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
        conn = self._get_conn()
        cursor = None
        if not conn:
            return False

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
            return True
        except mysql.connector.Error as e:
            conn.rollback()
            print(f"Error Create Transaksi: {e}")
            return False
        finally:
            if cursor is not None:
                cursor.close()
            conn.close()

    # UPDATE: Memperbarui transaksi
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
        conn = self._get_conn()
        cursor = None
        if not conn:
            return False

        try:
            if not self.get_transaksi_by_id(id_transaksi):
                return False

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
            return cursor.rowcount > 0
        except mysql.connector.Error as e:
            conn.rollback()
            print(f"Error Update Transaksi: {e}")
            return False
        finally:
            if cursor is not None:
                cursor.close()
            conn.close()

    # UPDATE: Memperbarui status cucian
    def update_status(self, id_transaksi, status_cucian):
        conn = self._get_conn()
        cursor = None
        if not conn:
            return False

        try:
            if not self.get_transaksi_by_id(id_transaksi):
                return False

            cursor = conn.cursor()
            query = (
                f"UPDATE {self.table_name} "
                "SET status_cucian = %s WHERE id_transaksi = %s"
            )
            cursor.execute(query, (status_cucian, id_transaksi))
            conn.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as e:
            conn.rollback()
            print(f"Error Update Status Transaksi: {e}")
            return False
        finally:
            if cursor is not None:
                cursor.close()
            conn.close()

    # DELETE: Menghapus transaksi
    def delete_transaksi(self, id_transaksi):
        conn = self._get_conn()
        cursor = None
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            query = f"DELETE FROM {self.table_name} WHERE id_transaksi = %s"
            cursor.execute(query, (id_transaksi,))
            conn.commit()
            return cursor.rowcount > 0
        except mysql.connector.Error as e:
            conn.rollback()
            print(f"Error Delete Transaksi: {e}")
            return False
        finally:
            if cursor is not None:
                cursor.close()
            conn.close()
