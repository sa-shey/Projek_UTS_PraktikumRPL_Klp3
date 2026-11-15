
import hashlib
import mysql.connector
from config.database import Database


class UserModel:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
        self.table_name = "users"

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def autentikasi(self, username, password):
        if not self.conn:
            return None

        try:
            cursor = self.conn.cursor(dictionary=True)
            password_hash = self.hash_password(password)

            query = (
                f"SELECT id_user, username, role FROM {self.table_name} "
                "WHERE username = %s AND password = %s"
            )
            cursor.execute(query, (username, password_hash))
            user = cursor.fetchone()
            cursor.close()
            return user

        except mysql.connector.Error as e:
            print(f"Error autentikasi: {e}")
            return None

    def username_exists(self, username):
        if not self.conn:
            return False

        try:
            cursor = self.conn.cursor()
            query = f"SELECT 1 FROM {self.table_name} WHERE username = %s"
            cursor.execute(query, (username,))
            ada = cursor.fetchone() is not None
            cursor.close()
            return ada

        except mysql.connector.Error as e:
            print(f"Error cek username: {e}")
            return False

    def register_user(self, username, password, role="user"):
        if not self.conn:
            return False

        try:
            cursor = self.conn.cursor()
            query = (
                f"INSERT INTO {self.table_name} (username, password, role) "
                "VALUES (%s, %s, %s)"
            )
            cursor.execute(
                query,
                (username, self.hash_password(password), role)
            )
            self.conn.commit()
            cursor.close()
            return True

        except mysql.connector.Error as e:
            print(f"Error register_user: {e}")
            self.conn.rollback()
            return False

    def register_customer(self, nama, no_telp, alamat, username, password):
        """Menyimpan akun customer dan data pelanggannya sekaligus."""
        if not self.conn:
            return False

        cursor = None

        try:
            cursor = self.conn.cursor()

            # 1. Simpan akun ke tabel users
            query_user = (
                "INSERT INTO users (username, password, role) "
                "VALUES (%s, %s, %s)"
            )
            cursor.execute(
                query_user,
                (username, self.hash_password(password), "customer")
            )

            # Ambil ID akun yang baru dibuat
            id_user = cursor.lastrowid

            # 2. Simpan identitas ke tabel pelanggan
            query_pelanggan = (
                "INSERT INTO pelanggan (id_user, nama, no_telp, alamat) "
                "VALUES (%s, %s, %s, %s)"
            )
            cursor.execute(
                query_pelanggan,
                (id_user, nama, no_telp or None, alamat or None)
            )

            # Simpan kedua perubahan sekaligus
            self.conn.commit()
            return True

        except mysql.connector.Error as e:
            print(f"Error register_customer: {e}")
            self.conn.rollback()
            return False

        finally:
            if cursor:
                cursor.close()
