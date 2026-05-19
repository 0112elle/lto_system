import sys
import pymysql

class MariaDBInstance:
    def __init__(self, user: str, password: str, database: str, host: str = "127.0.0.1", port: int = 3306):
        try:
            self.conn = pymysql.connect(
                user=user,
                password=password,
                host=host,
                port=port,
                database=database,
                autocommit=False,
                charset='utf8mb4'
            )
        except pymysql.Error as e:
            print(f"Error connecting to MariaDB: {e}")
            sys.exit(1)

        self.cursor = self.conn.cursor()

    def cur(self):
        return self.cursor

    def commit(self):
        try:
            self.conn.commit()
        except Exception:
            pass

    def rollback(self):
        try:
            self.conn.rollback()
        except Exception:
            pass

    def close(self):
        try:
            self.cursor.close()
        except Exception:
            pass
        try:
            self.conn.close()
        except Exception:
            pass
