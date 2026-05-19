from controller.driver_controller import DriverController
from controller.vehicle_controller import VehicleController
from controller.registration_controller import RegistrationController
from controller.violation_controller import ViolationController
from model.driver import Driver
from model.vehicle import Vehicle
from sql.sql_connector import MariaDBInstance
from view.formatters import format_license, format_registration, format_violation
from view.validators import read_int, read_date, read_float, read_str
from view.table import render_table

class UserInterface:
    def __init__(self, driver_ctrl: DriverController, vehicle_ctrl: VehicleController, registration_ctrl: RegistrationController, violation_ctrl: ViolationController):
        self.driver_ctrl = driver_ctrl
        self.vehicle_ctrl = vehicle_ctrl
        self.registration_ctrl = registration_ctrl
        self.violation_ctrl = violation_ctrl

    def print_main_menu(self):
        print("""=========================================================================================
\nWELCOME TO THE LTO SYSTEM\n
[1] Driver Management
[2] Vehicle Management
[3] Vehicle Registration Management
[4] Traffic Violation Management
[5] Generate Reports
[0] Exit
""")

    def driver_menu(self):
        while True:
            print('=========================================================================================')
            print('''\nDRIVER MANAGEMENT\n[1] Add driver\n[2] Update driver\n[3] Delete driver\n[4] Search driver\n[5] View driver details\n[0] Return\n''')
            c = input('Choice: ').strip()
            if c == '1':
                self.add_driver()
            elif c == '3':
                self.delete_driver()
            elif c == '4':
                self.search_driver()
            elif c == '5':
                self.view_driver_details()
            elif c == '0':
                return
            else:
                print('Not implemented or invalid')

    def registration_menu(self):
        while True:
            print('=========================================================================================')
            print('\nVEHICLE REGISTRATION MANAGEMENT\n[1] Add registration\n[2] Renew registration\n[3] Update registration\n[4] Delete registration\n[0] Return\n')
            c = input('Choice: ').strip()
            if c == '1':
                self.add_registration()
            elif c == '2':
                self.renew_registration()
            elif c == '3':
                self.update_registration()
            elif c == '4':
                self.delete_registration()
            elif c == '0':
                return
            else:
                print('Invalid')

    def add_registration(self):
        reg_no = read_str('Registration number: ')
        reg_date = read_date('Registration date (YYYY-MM-DD): ')
        exp_date = read_date('Expiration date (YYYY-MM-DD): ')
        status = read_str('Registration status (active/expired/suspended): ') or 'active'
        or_no = read_str('Official receipt number: ')
        or_date = read_date('Official receipt date (YYYY-MM-DD): ')
        doc_ref = read_str('Document ref no (optional): ', allow_blank=True)
        ownership = read_str('Ownership type (owned/financed/leased): ') or 'owned'
        transfer = read_str('Transfer reason (optional): ', allow_blank=True)
        owner_start = read_date('Ownership start date (YYYY-MM-DD): ', allow_blank=True) or reg_date
        owner_end = read_date('Ownership end date (YYYY-MM-DD) or blank: ', allow_blank=True)
        vehicle_id = read_int('Vehicle ID: ')
        params = (reg_no, reg_date, exp_date, status, or_no, or_date, doc_ref, ownership, transfer, owner_start, owner_end, vehicle_id)
        new = self.registration_ctrl.add_registration(params)
        print('Inserted registration: ' + str(new) if new else 'Insert failed')

    def renew_registration(self):
        old = read_str('Old registration number: ')
        new = read_str('New registration number: ')
        reg_date = read_date('Registration date (YYYY-MM-DD): ')
        exp_date = read_date('Expiration date (YYYY-MM-DD): ')
        or_no = read_str('Official receipt number: ')
        or_date = read_date('Official receipt date (YYYY-MM-DD): ')
        res = self.registration_ctrl.renew_registration(old, new, reg_date, exp_date, or_no, or_date)
        print('Renewed to: ' + str(res) if res else 'Renew failed')

    def update_registration(self):
        print('Update registration NOT fully implemented via UI')

    def delete_registration(self):
        rn = input('Registration number to delete: ').strip()
        ok = self.registration_ctrl.delete_registration(rn)
        print('Deleted' if ok else 'Delete failed')

    def violation_menu(self):
        while True:
            print('=========================================================================================')
            print('\nTRAFFIC VIOLATION MANAGEMENT\n')
            print('[1] Add violation')
            print('[2] Update violation')
            print('[3] Delete violation')
            print('[4] Search violations')
            print('[0] Return\n')
            c = input('Choice: ').strip()
            
            if c == '1':
                self.add_violation()
            elif c == '2':
                self.update_violation()
            elif c == '3':
                self.delete_violation()
            elif c == '4':
                self.search_violations()
            elif c == '0':
                return
            else:
                print('Invalid')

    def add_violation(self):
        print('Enter violation details:')
        vid = read_int('Driver ID: ')
        vehicle_id = read_int('Vehicle ID: ')
        vdate = read_date('Violation date (YYYY-MM-DD): ')
        vtype = read_int('Violation type id: ')
        fine = read_float('Fine amount: ')
        params = (vdate, 'unpaid', fine, None, vid, vehicle_id, vtype, 1, 1)  # adjust to proc signature
        new = self.violation_ctrl.add_violation(params)
        print('Inserted violation id ' + str(new) if new else 'Insert failed')

    def update_violation(self):
        vid = read_int('Violation ID to update: ')
        if vid is None:
            print('Invalid ID')
            return
        row = self.violation_ctrl.get_violation_by_id(vid)
        if not row:
            print('Violation not found')
            return
        # show existing info using formatter if possible
        try:
            print(format_violation(row))
        except Exception:
            print(row)

        confirm = read_str('Update this violation? (Y/n): ').strip() or 'Y'
        if confirm.lower().startswith('n'):
            print('Aborted')
            return

        # prompt for new status
        print('Select new status: [1] unpaid [2] paid [3] contested [0] leave unchanged')
        s = input('Choice: ').strip()
        status_map = {'1': 'unpaid', '2': 'paid', '3': 'contested'}
        new_status = None
        if s in status_map:
            new_status = status_map[s]

        payment_date = None
        if new_status == 'paid':
            payment_date = read_date('Payment date (YYYY-MM-DD): ')

        params = (vid, new_status, payment_date)
        ok = self.violation_ctrl.update_violation(params)
        print('Updated' if ok else 'Update failed')

    def delete_violation(self):
        try:
            vid = int(input('Violation ID to delete: ').strip())
        except Exception:
            print('Invalid')
            return
        ok = self.violation_ctrl.delete_violation(vid)
        print('Deleted' if ok else 'Delete failed')

    def search_violations(self):
        plate = input('Plate (blank skip): ').strip() or None
        driver = input('Driver ID (blank skip): ').strip() or None
        driver_id = int(driver) if driver else None
        rows = self.violation_ctrl.search_violation(plate, driver_id)
        for r in rows:
            print(format_violation(r))

    def reports_menu(self):
        while True:
            print('=========================================================================================')
            print('\nGENERATE REPORTS\n')
            print('[1] View All Registered Drivers')
            print('[2] View All Vehicles Owned by a Given Driver')
            print('[3] View All Vehicles with Expired Registrations as of a Given Date')
            print('[4] View All Drivers with Expired or Suspended Licenses')
            print('[5] View All Traffic Violations Committed by a Given Driver Within Specific Dates')
            print('[6] View Total Number of Violations per Violation Type for a Given Year')
            print('[7] View All Vehicle Involved in violations Within a Given City or Region')
            print('[0] Return\n')
            c = input('Choice: ').strip()
            if c == '1':
                # present filter submenu per UI_Ideas.txt
                while True:
                    print('_________________________________________________________________________________________')
                    print('\nGENERATE REPORTS: VIEW REGISTERED DRIVERS\n')
                    print('[1] License Type')
                    print('[2] License Status')
                    print('[3] Age Range')
                    print('[4] Sex Assigned at Birth')
                    print('[0] Return')
                    choice = input('Select which filter to be used: ').strip()
                    if choice == '0':
                        break
                    cur = self.driver_ctrl.db.cur()
                    if choice == '1':
                        print('_________________________________________________________________________________________')
                        print('\nSELECT LICENSE TYPE FILTER:\n')
                        print('[1] Student Permit')
                        print('[2] Professional')
                        print('[3] Non-Professional')
                        print('[0] Return')
                        lt = input('Enter License Type Filter (0-3): ').strip()
                        if lt == '0':
                            continue
                        mapping = {'1': 'Student Permit', '2': 'Professional', '3': 'Non-Professional'}
                        license_type = mapping.get(lt)
                        if not license_type:
                            print('Invalid selection')
                            continue
                        license_status = None
                        min_age = None
                        max_age = None
                        sex = None
                    elif choice == '2':
                        print('_________________________________________________________________________________________')
                        print('\nSELECT LICENSE STATUS FILTER:\n')
                        print('[1] Valid')
                        print('[2] Expired')
                        print('[3] Suspended')
                        print('[4] Revoked')
                        print('[0] Return')
                        ls = input('Enter License Status Filter (0-4): ').strip()
                        if ls == '0':
                            continue
                        mapping = {'1': 'Valid', '2': 'Expired', '3': 'Suspended', '4': 'Revoked'}
                        license_status = mapping.get(ls)
                        if not license_status:
                            print('Invalid selection')
                            continue
                        license_type = None
                        min_age = None
                        max_age = None
                        sex = None
                    elif choice == '3':
                        print('_________________________________________________________________________________________')
                        print('\nEnter Minimum and Maximum Age Bracket:')
                        while True:
                            min_age = read_int('Enter Minimum Age Bracket: ')
                            if min_age is None or min_age < 0:
                                print('Minimum age must be a non-negative integer')
                                continue
                            break
                        while True:
                            max_age = read_int('Enter Maximum Age Bracket: ')
                            if max_age is None or max_age < min_age:
                                print('Maximum age must be >= minimum age')
                                continue
                            break
                        license_type = None
                        license_status = None
                        sex = None
                    elif choice == '4':
                        print('_________________________________________________________________________________________')
                        print('\nSELECT SEX ASSIGNED AT BIRTH AS FILTER:')
                        print('[1] Male')
                        print('[2] Female')
                        print('[0] Return')
                        s = input('Enter Sex Assigned at Birth as Filter (0-2): ').strip()
                        if s == '0':
                            continue
                        mapping = {'1': 'Male', '2': 'Female'}
                        sex = mapping.get(s)
                        if not sex:
                            print('Invalid selection')
                            continue
                        license_type = None
                        license_status = None
                        min_age = None
                        max_age = None
                    else:
                        print('Invalid')
                        continue

                    # call stored procedure with selected filters
                    cur.callproc('GetDriversByFilters', (license_type, license_status, min_age, max_age, sex))
                    rows = cur.fetchall()
                    if rows:
                        # use the cursor description to display all returned columns
                        headers = [d[0] for d in cur.description] if cur.description else [f'col{i}' for i in range(len(rows[0]))]
                        render_table(headers, rows)

                        # additionally show full driver record + full license details from model/procs
                        # This fetches canonical driver fields (from vw_driver via get_driver_by_id) and licenses
                        # so the output contains all schema attributes even if the filter proc returns fewer columns.
                        driver_id_idx = None
                        # try to find Driver_id column index
                        for i, h in enumerate(headers):
                            if h.lower() in ('driver_id', 'driverid', 'id'):
                                driver_id_idx = i
                                break

                        if driver_id_idx is not None:
                            # ensure rows are ordered by driver id ascending for predictable output
                            try:
                                rows_list = list(rows)
                            except Exception:
                                rows_list = rows

                            # sort by detected driver id index if possible
                            try:
                                rows_sorted = sorted(rows_list, key=lambda r: (r[driver_id_idx] if r[driver_id_idx] is not None else 0))
                            except Exception:
                                rows_sorted = rows_list

                            for row in rows_sorted:
                                try:
                                    did = row[driver_id_idx]
                                except Exception:
                                    continue
                                full = self.driver_ctrl.get_driver_by_id(did)
                                if full:
                                    # print driver without trailing newline to avoid extra blank line
                                    print(str(full).rstrip('\n'))
                                    licenses = self.driver_ctrl.get_driver_licenses(did)
                                    if licenses:
                                        if len(licenses) > 1:
                                            print('Warning: multiple license records found; showing the first one')
                                        lic = licenses[0]
                                        ln = lic[0] or '-'
                                        lic_type = lic[1] if len(lic) > 1 else None
                                        lic_status = lic[2] if len(lic) > 2 else None
                                        issued = lic[3] if len(lic) > 3 else None
                                        expiry = lic[4] if len(lic) > 4 else None
                                        dlcodes = lic[5] if len(lic) > 5 else None
                                        conds = lic[6] if len(lic) > 6 else None
                                        print('License No.:   ', ln)
                                        print('License Type:  ', lic_type or '-')
                                        print('License Status:', lic_status or '-')
                                        print('Issued:        ', issued or '-')
                                        print('Expiry:        ', expiry or '-')
                                        print('DL Codes:      ', dlcodes or 'N/A')
                                        print('Conditions:    ', conds if conds else 'N/A')
                                    else:
                                        print('No license records found')
                                else:
                                    print(f'Could not fetch full driver record for id {did}')
                        else:
                            print('\nNote: returned rows do not include a driver identifier; full driver details cannot be retrieved automatically.')
                    else:
                        print('No drivers found for the selected filter')
            elif c == '2':
                try:
                    did = int(input('Driver ID: ').strip())
                except Exception:
                    print('Invalid')
                    continue
                rows = self.driver_ctrl.get_driver_vehicles(did)
                if rows:
                    headers = ['Vehicle ID','Plate','Engine','Chassis','Make','Model']
                    render_table(headers, rows)
                    # additionally show full vehicle details and related records
                    # try to find vehicle id column index in our headers
                    vehicle_id_idx = None
                    for i, h in enumerate(headers):
                        if h.lower().replace(' ', '_') in ('vehicle_id','vehicleid','id'):
                            vehicle_id_idx = i
                            break

                    if vehicle_id_idx is not None:
                        try:
                            rows_list = list(rows)
                        except Exception:
                            rows_list = rows
                        try:
                            rows_sorted = sorted(rows_list, key=lambda r: (r[vehicle_id_idx] if r[vehicle_id_idx] is not None else 0))
                        except Exception:
                            rows_sorted = rows_list

                        for row in rows_sorted:
                            try:
                                vid = row[vehicle_id_idx]
                            except Exception:
                                continue
                            full = None
                            try:
                                full = self.vehicle_ctrl.get_vehicle_by_id(vid)
                            except Exception:
                                full = None
                            if full:
                                # print vehicle summary
                                vid, eng, plate, chas, vtype, make, model, year, body, cap, color, owner = full
                                print("------------------------------------------------------------------------------------")
                                print('Vehicle ID:  ', vid)
                                print('Make:        ', make)
                                print('Model:       ', model)
                                print('Type:        ', vtype)
                                print('Plate:       ', plate or '-')
                                print('Engine:      ', eng or '-')
                                print('Chassis:     ', chas or '-')
                                print('Year:        ', year or '-')
                                print('Body type:   ', body or '-')
                                print('Capacity:    ', cap or '-')
                                print('Color:       ', color or '-')
                                # (Registrations and violations intentionally omitted for this report)
                                print('')
                            else:
                                print(f'Could not fetch full vehicle for id {vid}')
                else:
                    print('No vehicles found')
            elif c == '3':
                date = input('As of date (YYYY-MM-DD): ').strip()
                rows = self.registration_ctrl.get_expired_registrations(date)
                if rows:
                    headers = ['Reg No','Reg Date','Expiry','Status','OR No','OR Date','Vehicle ID']
                    render_table(headers, rows)
                else:
                    print('No expired registrations')
            elif c == '4':
                cur = self.driver_ctrl.db.cur()
                cur.execute('SELECT * FROM ExpiredOrSuspendedLicenses')
                rows = cur.fetchall()
                if rows:
                    headers = [desc[0] for desc in cur.description]
                    render_table(headers, rows)
                else:
                    print('No licenses found')
            elif c == '5':
                try:
                    did = int(input('Driver ID: ').strip())
                except Exception:
                    print('Invalid')
                    continue
                start = input('Start date (YYYY-MM-DD): ').strip()
                end = input('End date (YYYY-MM-DD): ').strip()
                rows = self.violation_ctrl.get_violations_by_driver_and_range(did, start, end)
                if rows:
                    headers = ['Violation ID','Date','Fine','Status','Type','Plate','City','Region']
                    render_table(headers, rows)
                else:
                    print('No violations found')
            elif c == '6':
                year = int(input('Year (YYYY): ').strip())
                cur = self.driver_ctrl.db.cur()
                cur.callproc('GetViolationCountsByTypePerYear', (year,))
                rows = cur.fetchall()
                if rows:
                    headers = [desc[0] for desc in cur.description]
                    render_table(headers, rows)
                else:
                    print('No data')
            elif c == '7':
                city = input('City (blank skip): ').strip() or None
                region = input('Region (blank skip): ').strip() or None
                cur = self.driver_ctrl.db.cur()
                cur.callproc('GetViolatedVehiclesByLocation', (city, region))
                rows = cur.fetchall()
                if rows:
                    headers = [desc[0] for desc in cur.description]
                    render_table(headers, rows)
                else:
                    print('No vehicles found')
            elif c == '0':
                return
            else:
                print('Invalid')

    def add_driver(self):
        print('Enter new driver (minimal):')
        first = input('First name: ').strip()
        last = input('Last name: ').strip()
        dob = input('Date of birth (YYYY-MM-DD): ').strip()
        d = Driver(First_name=first, Last_name=last, Date_of_birth=dob)
        new_id = self.driver_ctrl.insert_driver(d)
        if new_id:
            print(f'Inserted driver id {new_id}')
        else:
            print('Insert failed')

    def delete_driver(self):
        try:
            did = int(input('Driver ID to delete: ').strip())
        except Exception:
            print('Invalid ID')
            return
        ok = self.driver_ctrl.delete_driver_by_id(did)
        print('Deleted' if ok else 'Delete failed')

    def search_driver(self):
        first = input('First name (blank skip): ').strip() or None
        last = input('Last name (blank skip): ').strip() or None
        contact = input('Contact (blank skip): ').strip() or None
        res = self.driver_ctrl.search_drivers(first, last, contact)
        for r in res:
            print(r)

    def view_driver_details(self):
        try:
            did = int(input('Driver ID: ').strip())
        except Exception:
            print('Invalid ID')
            return
        d = self.driver_ctrl.get_driver_by_id(did)
        if not d:
            print('Driver not found')
            return
        print(str(d).rstrip('\n'))
        print('\nOwned Vehicles:')
        for v in self.driver_ctrl.get_driver_vehicles(did):
            print(v)
        print('\nLicenses:')
        licenses = self.driver_ctrl.get_driver_licenses(did)
        if licenses:
            for lic in licenses:
                try:
                    print(format_license(lic))
                except Exception:
                    print(lic)
        else:
            print('No license records found')
        print('\nViolations:')
        for tv in self.driver_ctrl.get_driver_violations(did):
            print(tv)

    def vehicle_menu(self):
        while True:
            print('=========================================================================================')
            print('''\nVEHICLE MANAGEMENT\n[1] Add vehicle\n[2] Update vehicle\n[3] Delete vehicle\n[4] Search vehicle\n[5] View vehicle details\n[0] Return\n''')
            c = input('Choice: ').strip()
            if c == '1':
                self.add_vehicle()
            elif c == '4':
                self.search_vehicle()
            elif c == '5':
                self.view_vehicle_details()
            elif c == '0':
                return
            else:
                print('Not implemented or invalid')

    def add_vehicle(self):
        plate = input('Plate number: ').strip()
        engine = input('Engine number: ').strip()
        chassis = input('Chassis number: ').strip()
        v = Vehicle(Plate_number=plate, Engine_number=engine, Chassis_number=chassis)
        new_id = self.vehicle_ctrl.add_vehicle(v)
        print('Inserted vehicle id ' + str(new_id) if new_id else 'Insert failed')

    def search_vehicle(self):
        plate = input('Plate (blank skip): ').strip() or None
        last = input('Owner last name (blank skip): ').strip() or None
        vtype = input('Vehicle type (blank skip): ').strip() or None
        res = self.vehicle_ctrl.search_vehicle(plate, last, vtype)
        for r in res:
            print(r)

    def view_vehicle_details(self):
        try:
            vid = int(input('Vehicle ID: ').strip())
        except Exception:
            print('Invalid ID')
            return
        owner = self.vehicle_ctrl.get_vehicle_owner(vid)
        print('Owner: ', owner)
        print('Registrations:')
        for reg in self.vehicle_ctrl.get_vehicle_registrations(vid):
            print(reg)
        print('Violations:')
        for tv in self.vehicle_ctrl.get_vehicle_violations(vid):
            print(tv)

    def start(self):
        while True:
            self.print_main_menu()
            c = input('Enter option: ').strip()
            if c == '1':
                self.driver_menu()
            elif c == '2':
                self.vehicle_menu()
            elif c == '3':
                self.registration_menu()
            elif c == '4':
                self.violation_menu()
            elif c == '5':
                self.reports_menu()
            elif c == '0':
                print('Goodbye')
                return
            else:
                print('Invalid')
