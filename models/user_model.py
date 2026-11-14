import hashlib
from mysql.connector import Error
from config.database import Database


class UserModel:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
        self.table_name = "users"

    @staticmethod
    def hash_password(password):
        # Mengubah plain text password menjadi hash SHA-256 (64 karakter hex)
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def autentikasi(self, username, password):
        """Mengembalikan dict {id_user, username, role} jika cocok, selain itu None."""
        if not self.conn:
            return None
        try:
            cursor = self.conn.cursor(dictionary=True)
            password_hash = self.hash_password(password)
            # Parameterized query untuk mencegah SQL Injection
            query = (f"SELECT id_user, username, role FROM {self.table_name} "
                     "WHERE username = %s AND password = %s")
            cursor.execute(query, (username, password_hash))
            user = cursor.fetchone()
            cursor.close()
            return user
        except Error as e:
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
        except Error as e:
            print(f"Error cek username: {e}")
            return False

    def register_user(self, username, password, role="user"):
        """Menyimpan akun baru; password otomatis di-hash SHA-256 sebelum disimpan."""
        if not self.conn:
            return False
        try:
            cursor = self.conn.cursor()
            query = (f"INSERT INTO {self.table_name} (username, password, role) "
                     "VALUES (%s, %s, %s)")
            cursor.execute(query, (username, self.hash_password(password), role))
            self.conn.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"Error register_user: {e}")
            self.conn.rollback()
            return False
