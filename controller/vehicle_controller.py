from typing import List, Optional
from sql.sql_connector import MariaDBInstance
from model.vehicle import Vehicle

class VehicleController:
    def __init__(self, db: MariaDBInstance):
        self.db = db

    def add_vehicle(self, v: Vehicle) -> Optional[int]:
        cur = self.db.cur()
        try:
            params = (
                v.Engine_number, v.Plate_number, v.Chassis_number, v.Vehicle_type, v.Make, v.Model, v.Year, v.Body_type, v.Capacity, v.Color, v.Driver_id
            )
            cur.callproc('AddVehicle', params)
            rows = cur.fetchall()
            new_id = None
            if rows and len(rows) > 0:
                first = rows[0]
                if isinstance(first, (list, tuple)) and len(first) > 0:
                    new_id = first[0]
            self.db.commit()
            return new_id
        except Exception as e:
            print(f"DB error during add vehicle: {e}")
            self.db.rollback()
            return None

    def update_vehicle(self, v: Vehicle) -> Optional[int]:
        cur = self.db.cur()
        try:
            params = (v.Vehicle_id, v.Engine_number, v.Plate_number, v.Chassis_number, v.Vehicle_type, v.Make, v.Model, v.Year, v.Body_type, v.Capacity, v.Color, v.Driver_id)
            cur.callproc('UpdateVehicle', params)
            rows = cur.fetchall()
            self.db.commit()
            return rows
        except Exception as e:
            print(f"DB error during update vehicle: {e}")
            self.db.rollback()
            return None

    def delete_vehicle(self, vehicle_id: int) -> bool:
        cur = self.db.cur()
        try:
            cur.callproc('DeleteVehicle', (vehicle_id,))
            rows = cur.fetchall()
            self.db.commit()
            return True
        except Exception as e:
            print(f"DB error during delete vehicle: {e}")
            self.db.rollback()
            return False

    def search_vehicle(self, plate: Optional[str], owner_last: Optional[str], vehicle_type: Optional[str]) -> List[Vehicle]:
        cur = self.db.cur()
        try:
            cur.callproc('SearchVehicle', (plate, owner_last, vehicle_type))
            rows = cur.fetchall()
            results = []
            for r in rows:
                results.append(Vehicle(Vehicle_id=r[0], Engine_number=r[1], Plate_number=r[2], Chassis_number=r[3], Vehicle_type=r[4], Make=r[5], Model=r[6], Year=r[7], Body_type=r[8], Capacity=r[9], Color=r[10], Driver_id=r[11]))
            return results
        except Exception as e:
            print(f"DB error during search vehicle: {e}")
            return []

    def get_vehicle_owner(self, vehicle_id: int):
        cur = self.db.cur()
        cur.callproc('GetVehicleOwner', (vehicle_id,))
        return cur.fetchall()

    def get_vehicle_registrations(self, vehicle_id: int):
        cur = self.db.cur()
        cur.callproc('GetVehicleRegistrations', (vehicle_id,))
        return cur.fetchall()

    def get_vehicle_violations(self, vehicle_id: int):
        cur = self.db.cur()
        cur.callproc('GetVehicleViolations', (vehicle_id,))
        return cur.fetchall()

    def get_vehicle_by_id(self, vehicle_id: int):
        cur = self.db.cur()
        try:
            cur.execute('SELECT Vehicle_id, Engine_number, Plate_number, Chassis_number, Vehicle_type, Make, Model, Year, Body_type, Capacity, Color, Driver_id FROM VEHICLE WHERE Vehicle_id=%s', (vehicle_id,))
            return cur.fetchone()
        except Exception as e:
            print(f"DB error get vehicle by id: {e}")
            return None
