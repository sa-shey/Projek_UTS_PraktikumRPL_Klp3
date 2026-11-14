
from config.database import Database


class PelangganModel:

    def __init__(self):
        self.db = Database()

    # READ: Menampilkan semua pelanggan
    def tampilkan_pelanggan(self):
        conn = self.db.get_connection()

        if conn is None:
            return []

        try:
            cursor = conn.cursor(dictionary=True)

            query = "SELECT * FROM pelanggan ORDER BY id_pelanggan"
            cursor.execute(query)

            data = cursor.fetchall()
            return data

        except Exception as e:
            print(f"Error tampilkan pelanggan: {e}")
            return []

        finally:
            cursor.close()
            conn.close()

    # CREATE: Menambahkan pelanggan
    def tambah_pelanggan(self, id_pelanggan, nama, alamat, no_hp):
        conn = self.db.get_connection()

        if conn is None:
            return False

        try:
            cursor = conn.cursor()

            query = """
                INSERT INTO pelanggan
                (id_pelanggan, nama, alamat, no_hp)
                VALUES (%s, %s, %s, %s)
            """

            values = (id_pelanggan, nama, alamat, no_hp)

            cursor.execute(query, values)
            conn.commit()

            return True

        except Exception as e:
            print(f"Error tambah pelanggan: {e}")
            conn.rollback()
            return False

        finally:
            cursor.close()
            conn.close()

    # UPDATE: Memperbarui data pelanggan
    def update_pelanggan(self, id_pelanggan, nama, alamat, no_hp):
        conn = self.db.get_connection()

        if conn is None:
            return False

        try:
            cursor = conn.cursor()

            query = """
                UPDATE pelanggan
                SET nama = %s,
                    alamat = %s,
                    no_hp = %s
                WHERE id_pelanggan = %s
            """

            values = (nama, alamat, no_hp, id_pelanggan)

            cursor.execute(query, values)
            conn.commit()

            return cursor.rowcount > 0

        except Exception as e:
            print(f"Error update pelanggan: {e}")
            conn.rollback()
            return False

        finally:
            cursor.close()
            conn.close()

    # DELETE: Menghapus pelanggan
    def hapus_pelanggan(self, id_pelanggan):
        conn = self.db.get_connection()

        if conn is None:
            return False

        try:
            cursor = conn.cursor()

            query = """
                DELETE FROM pelanggan
                WHERE id_pelanggan = %s
            """

            cursor.execute(query, (id_pelanggan,))
            conn.commit()

            return cursor.rowcount > 0

        except Exception as e:
            print(f"Error hapus pelanggan: {e}")
            conn.rollback()
            return False

        finally:
            cursor.close()
            conn.close()
