
from config.database import Database


class PaketModel:

    def __init__(self):
        self.db = Database()

    # READ: Menampilkan semua paket layanan
    def tampilkan_paket(self):
        conn = self.db.get_connection()

        if conn is None:
            return []

        try:
            cursor = conn.cursor(dictionary=True)

            query = "SELECT * FROM paket_layanan ORDER BY id_paket"
            cursor.execute(query)

            data = cursor.fetchall()
            return data

        except Exception as e:
            print(f"Error tampilkan paket: {e}")
            return []

        finally:
            cursor.close()
            conn.close()

    # CREATE: Menambahkan paket layanan
    def tambah_paket(self, id_paket, nama_paket, jenis, harga_per_kg):
        conn = self.db.get_connection()

        if conn is None:
            return False

        try:
            cursor = conn.cursor()

            query = """
                INSERT INTO paket_layanan
                (id_paket, nama_paket, jenis, harga_per_kg)
                VALUES (%s, %s, %s, %s)
            """

            values = (id_paket, nama_paket, jenis, harga_per_kg)

            cursor.execute(query, values)
            conn.commit()

            return True

        except Exception as e:
            print(f"Error tambah paket: {e}")
            conn.rollback()
            return False

        finally:
            cursor.close()
            conn.close()

    # UPDATE: Memperbarui paket layanan
    def update_paket(self, id_paket, nama_paket, jenis, harga_per_kg):
        conn = self.db.get_connection()

        if conn is None:
            return False

        try:
            cursor = conn.cursor()

            query = """
                UPDATE paket_layanan
                SET nama_paket = %s,
                    jenis = %s,
                    harga_per_kg = %s
                WHERE id_paket = %s
            """

            values = (nama_paket, jenis, harga_per_kg, id_paket)

            cursor.execute(query, values)
            conn.commit()

            return cursor.rowcount > 0

        except Exception as e:
            print(f"Error update paket: {e}")
            conn.rollback()
            return False

        finally:
            cursor.close()
            conn.close()

    # DELETE: Menghapus paket layanan
    def hapus_paket(self, id_paket):
        conn = self.db.get_connection()

        if conn is None:
            return False

        try:
            cursor = conn.cursor()

            query = """
                DELETE FROM paket_layanan
                WHERE id_paket = %s
            """

            cursor.execute(query, (id_paket,))
            conn.commit()

            return cursor.rowcount > 0

        except Exception as e:
            print(f"Error hapus paket: {e}")
            conn.rollback()
            return False

        finally:
            cursor.close()
            conn.close()
