from sql.sql_connector import MariaDBInstance
from controller.driver_controller import DriverController
from controller.vehicle_controller import VehicleController
from controller.registration_controller import RegistrationController
from controller.violation_controller import ViolationController
from view.ui import UserInterface
import os

def main():
    # configure via env or defaults
    user = os.environ.get('LTO_DB_USER', 'ltodirector')
    password = os.environ.get('LTO_DB_PASSWORD', 'lto')
    database = os.environ.get('LTO_DB_NAME', 'lto')

    db = MariaDBInstance(user=user, password=password, database=database)
    driver_ctrl = DriverController(db)
    vehicle_ctrl = VehicleController(db)
    registration_ctrl = RegistrationController(db)
    violation_ctrl = ViolationController(db)
    ui = UserInterface(driver_ctrl, vehicle_ctrl, registration_ctrl, violation_ctrl)
    try:
        ui.start()
    finally:
        db.close()

if __name__ == '__main__':
    main()
