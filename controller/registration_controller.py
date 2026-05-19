from typing import Optional, List
from sql.sql_connector import MariaDBInstance

class RegistrationController:
    def __init__(self, db: MariaDBInstance):
        self.db = db

    def add_registration(self, params: tuple) -> Optional[str]:
        cur = self.db.cur()
        try:
            cur.callproc('AddRegistration', params)
            rows = cur.fetchall()
            self.db.commit()
            if rows and len(rows)>0:
                return rows[0][0]
            return None
        except Exception as e:
            print(f"DB error add registration: {e}")
            self.db.rollback()
            return None

    def renew_registration(self, old_reg_no: str, new_reg_no: str, reg_date: str, exp_date: str, or_number: str, or_date: str) -> Optional[str]:
        cur = self.db.cur()
        try:
            cur.callproc('RenewRegistration', (old_reg_no, new_reg_no, reg_date, exp_date, or_number, or_date))
            rows = cur.fetchall()
            self.db.commit()
            if rows and len(rows)>0:
                return rows[0][0]
            return None
        except Exception as e:
            print(f"DB error renew registration: {e}")
            self.db.rollback()
            return None

    def update_registration(self, params: tuple) -> bool:
        cur = self.db.cur()
        try:
            cur.callproc('UpdateRegistration', params)
            rows = cur.fetchall()
            self.db.commit()
            return True
        except Exception as e:
            print(f"DB error update registration: {e}")
            self.db.rollback()
            return False

    def delete_registration(self, reg_number: str) -> bool:
        cur = self.db.cur()
        try:
            cur.callproc('DeleteRegistration', (reg_number,))
            rows = cur.fetchall()
            self.db.commit()
            return True
        except Exception as e:
            print(f"DB error delete registration: {e}")
            self.db.rollback()
            return False

    def search_registration(self, reg_number: Optional[str], plate: Optional[str]) -> List[tuple]:
        cur = self.db.cur()
        try:
            cur.callproc('SearchRegistration', (reg_number, plate))
            rows = cur.fetchall()
            return rows
        except Exception as e:
            print(f"DB error search registration: {e}")
            return []

    def get_expired_registrations(self, as_of_date: str) -> List[tuple]:
        cur = self.db.cur()
        try:
            cur.callproc('GetExpiredRegistrations', (as_of_date,))
            rows = cur.fetchall()
            return rows
        except Exception as e:
            print(f"DB error expired registrations: {e}")
            return []
