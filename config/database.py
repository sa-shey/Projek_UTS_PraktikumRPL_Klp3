
import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        self.host = "localhost"
        self.db_name = "db_laundry_uas"
        self.username = "root"
        self.password = ""
        self.port = 3306
        self.conn = None

    def get_connection(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                database=self.db_name,
                user=self.username,
                password=self.password,
                port=self.port
            )

            if self.conn.is_connected():
                print("Koneksi Database Berhasil!")
                return self.conn

        except Error as e:
            print(f"Koneksi Gagal: {e}")
            return None
