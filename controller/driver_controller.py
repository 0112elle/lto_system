from typing import List, Optional
from sql.sql_connector import MariaDBInstance
from model.driver import Driver
import datetime

class DriverController:
    def __init__(self, db: MariaDBInstance):
        self.db = db

    def get_all_drivers(self) -> List[Driver]:
        cur = self.db.cur()
        cur.execute("SELECT Driver_id, First_name, Middle_name, Last_name, Suffix, Date_of_birth, Weight, Height, Sex_assigned_at_birth, Nationality, Civil_status, Contact_number, Blood_type, House_number, Street_village, Barangay, City_municipality, Province, Region, Zip_code, License_number, License_type, License_status, Age FROM vw_driver ORDER BY Driver_id ASC")
        rows = cur.fetchall()
        results = []
        for r in rows:
            dob = r[5].isoformat() if hasattr(r[5], 'isoformat') else r[5]
            results.append(Driver(
                Driver_id=r[0], 
                First_name=r[1], Middle_name=r[2], Last_name=r[3], Suffix=r[4], 
                Date_of_birth=dob,
                Weight=r[6], 
                Height=r[7], 
                Sex_assigned_at_birth=r[8], 
                Nationality=r[9], 
                Civil_status=r[10], 
                Contact_number=r[11], 
                Blood_type=r[12],
                House_number=r[13], Street_village=r[14], Barangay=r[15], City_municipality=r[16], Province=r[17], Region=r[18], Zip_code=r[19],
                License_number=r[20], 
                License_type=r[21], 
                License_status=r[22], 
                Age=r[23]
            ))
        return results

    def get_driver_by_id(self, driver_id: int) -> Optional[Driver]:
        cur = self.db.cur()
        cur.execute("SELECT Driver_id, First_name, Middle_name, Last_name, Suffix, Date_of_birth, Weight, Height, Sex_assigned_at_birth, Nationality, Civil_status, Contact_number, Blood_type, House_number, Street_village, Barangay, City_municipality, Province, Region, Zip_code, License_number, License_type, License_status, Age FROM vw_driver WHERE Driver_id=%s", (driver_id,))
        row = cur.fetchone()
        if not row:
            return None
        dob = row[5].isoformat() if hasattr(row[5], 'isoformat') else row[5]
        return Driver(
            Driver_id=row[0], 
            First_name=row[1], Middle_name=row[2], Last_name=row[3], Suffix=row[4], 
            Date_of_birth=dob,
            Weight=row[6], 
            Height=row[7], 
            Sex_assigned_at_birth=row[8], 
            Nationality=row[9], 
            Civil_status=row[10], 
            Contact_number=row[11], 
            Blood_type=row[12],
            House_number=row[13], Street_village=row[14], Barangay=row[15], City_municipality=row[16], Province=row[17], Region=row[18], Zip_code=row[19],
            License_number=row[20], 
            License_type=row[21], 
            License_status=row[22], 
            Age=row[23]
        )

    def insert_driver(self, d: Driver) -> Optional[int]:
        cur = self.db.cur()
        try:
            params = (
                d.First_name, d.Middle_name, d.Last_name, d.Suffix, 
                d.Date_of_birth, 
                d.Weight, 
                d.Height, 
                d.Sex_assigned_at_birth,
                d.Nationality or 'Filipino', 
                d.Civil_status, 
                d.Contact_number, 
                d.Blood_type, 
                d.House_number, d.Street_village, d.Barangay, d.City_municipality, d.Province, d.Region, d.Zip_code
            )
            cur.callproc('AddDriver', params)
            rows = cur.fetchall()
            new_id = None
            if rows and len(rows) > 0:
                first = rows[0]
                if isinstance(first, (list, tuple)) and len(first) > 0:
                    new_id = first[0]
            self.db.commit()
            return new_id
        except Exception as e:
            print(f"DB error during insert: {e}")
            self.db.rollback()
            return None

    def delete_driver_by_id(self, driver_id: int) -> bool:
        cur = self.db.cur()
        try:
            cur.execute("SELECT 1 FROM DRIVER WHERE Driver_id=%s", (driver_id,))
            if cur.fetchone() is None:
                return False
            cur.callproc('DeleteDriver', (driver_id,))
            rows = cur.fetchall()
            self.db.commit()
            return True
        except Exception as e:
            print(f"DB error during delete: {e}")
            self.db.rollback()
            return False

    def search_drivers(self, first: Optional[str], last: Optional[str], contact: Optional[str]) -> List[Driver]:
        cur = self.db.cur()
        try:
            cur.callproc('SearchDriver', (first, last, None, contact))
            rows = cur.fetchall()
        except Exception as e:
            print(f"DB error during search: {e}")
            return []
        results = []
        for row in rows:
            dob = row[5].isoformat() if hasattr(row[5], 'isoformat') else row[5]
            age = None
            try:
                if dob:
                    age = datetime.date.today().year - datetime.date.fromisoformat(dob).year
            except Exception:
                age = None
            results.append(Driver(
                Driver_id=row[0], 
                First_name=row[1], Middle_name=row[2], Last_name=row[3], Suffix=row[4], 
                Date_of_birth=dob,
                Weight=row[6], 
                Height=row[7], 
                Sex_assigned_at_birth=row[8], 
                Nationality=row[9], 
                Civil_status=row[10], 
                Contact_number=row[11], 
                Blood_type=row[12],
                House_number=row[13], Street_village=row[14], Barangay=row[15], City_municipality=row[16], Province=row[17], Region=row[18], Zip_code=row[19],
                License_number=row[20] if len(row) > 20 else None, 
                License_type=row[21] if len(row) > 21 else None, 
                License_status=row[22] if len(row) > 22 else None, 
                Age=age
            ))
        return results

    def get_driver_vehicles(self, driver_id: int):
        cur = self.db.cur()
        cur.callproc('GetDriverVehicles', (driver_id,))
        return cur.fetchall()

    def get_driver_licenses(self, driver_id: int):
        cur = self.db.cur()
        cur.callproc('GetDriverLicenses', (driver_id,))
        return cur.fetchall()

    def get_driver_violations(self, driver_id: int):
        cur = self.db.cur()
        cur.callproc('GetDriverViolations', (driver_id,))
        return cur.fetchall()
