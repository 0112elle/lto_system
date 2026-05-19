LTO System (Console)
====================

This guide is for Ubuntu users who will run this project from scratch.

Prerequisites
-------------

- Ubuntu terminal access
- Internet connection (for package installs)
- Repository cloned locally

Step 1: Install Python 3 and venv tools
---------------------------------------

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
```

Verify Python is installed:

```bash
python3 --version
```

Step 2: Install MariaDB
-----------------------

```bash
sudo apt install -y mariadb-server mariadb-client
sudo systemctl enable mariadb
sudo systemctl start mariadb
```

Optional hardening (recommended on fresh installs):

```bash
sudo mysql_secure_installation
```

Step 3: Go to project folder
----------------------------

From your repository root:

```bash
cd lto_system
```

Step 4: Create and activate a virtual environment
-------------------------------------------------

Create venv:

```bash
python3 -m venv .venv
```

Activate venv:

```bash
source .venv/bin/activate
```

After activation, your prompt should show `(.venv)`.

Step 5: Install Python dependencies
-----------------------------------

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Step 6: Create database and load SQL_Statements.sql
---------------------------------------------------

Open MariaDB shell as root:

```bash
sudo mariadb
```

Inside MariaDB shell, run:

```sql
CREATE DATABASE IF NOT EXISTS lto;
CREATE USER IF NOT EXISTS 'lto_user'@'localhost' IDENTIFIED BY 'lto_password';
GRANT ALL PRIVILEGES ON lto.* TO 'lto_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

Then import schema + procedures:

```bash
mariadb -u lto_user -p lto < SQL_Statements.sql
```

Step 7: Set environment variables
---------------------------------

Set variables in the same terminal before running the app:

```bash
export LTO_DB_HOST=localhost
export LTO_DB_PORT=3306
export LTO_DB_USER=lto_user
export LTO_DB_PASSWORD=lto_password
export LTO_DB_NAME=lto
```

Optional check:

```bash
echo "$LTO_DB_USER $LTO_DB_NAME $LTO_DB_HOST $LTO_DB_PORT"
```

Step 8: Run the program
-----------------------

```bash
python3 main.py
```

Run Tests (Optional)
--------------------

From `lto_system` folder with venv activated:

```bash
pytest
```

Common Issues
-------------

- `mariadb: command not found`
	- Re-run: `sudo apt install -y mariadb-server mariadb-client`

- `Access denied for user`
	- Recheck `LTO_DB_USER` / `LTO_DB_PASSWORD`
	- Ensure privileges were granted on database `lto`

- `Unknown database 'lto'`
	- Create it first: `CREATE DATABASE lto;`

- `ModuleNotFoundError`
	- Ensure venv is active (`source .venv/bin/activate`)
	- Reinstall dependencies: `pip install -r requirements.txt`

Notes
-----

- Many controller methods call stored procedures. If the SQL file import fails, features that depend on procedures will fail.
- The console UI includes Drivers, Vehicles, Registrations, Violations, and Reports menus.
