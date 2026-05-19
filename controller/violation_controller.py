from typing import List, Optional
from sql.sql_connector import MariaDBInstance

class ViolationController:
    def __init__(self, db: MariaDBInstance):
        self.db = db

    def add_violation(self, params: tuple) -> Optional[int]:
        cur = self.db.cur()
        try:
            cur.callproc('AddViolation', params)
            rows = cur.fetchall()
            self.db.commit()
            if rows and len(rows)>0:
                return rows[0][0]
            return None
        except Exception as e:
            print(f"DB error add violation: {e}")
            self.db.rollback()
            return None

    def update_violation(self, params: tuple) -> bool:
        cur = self.db.cur()
        try:
            cur.callproc('UpdateViolation', params)
            rows = cur.fetchall()
            self.db.commit()
            return True
        except Exception as e:
            print(f"DB error update violation: {e}")
            self.db.rollback()
            return False

    def delete_violation(self, violation_id: int) -> bool:
        cur = self.db.cur()
        try:
            cur.callproc('DeleteViolation', (violation_id,))
            self.db.commit()
            return True
        except Exception as e:
            print(f"DB error delete violation: {e}")
            self.db.rollback()
            return False

    def search_violation(self, plate: Optional[str], driver_id: Optional[int]) -> List[tuple]:
        cur = self.db.cur()
        try:
            cur.callproc('SearchViolation', (plate, driver_id))
            rows = cur.fetchall()
            return rows
        except Exception as e:
            print(f"DB error search violation: {e}")
            return []

    def get_violations_by_driver_and_range(self, driver_id: int, start_date: str, end_date: str) -> List[tuple]:
        cur = self.db.cur()
        try:
            cur.callproc('GetViolationsByDriverAndDateRange', (driver_id, start_date, end_date))
            rows = cur.fetchall()
            return rows
        except Exception as e:
            print(f"DB error get violations by driver/date: {e}")
            return []

    def get_violation_by_id(self, violation_id: int):
        cur = self.db.cur()
        try:
            cur.execute('SELECT * FROM TRAFFIC_VIOLATION WHERE Violation_id=%s', (violation_id,))
            return cur.fetchone()
        except Exception as e:
            print(f"DB error get violation by id: {e}")
            return None
