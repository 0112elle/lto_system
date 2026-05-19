LTO System (Console)
=====================

This README now specifies where to run each command: Windows PowerShell/Command
Prompt, Ubuntu (or WSL), or the MariaDB shell. Also shows when to `cd` into the
`lto_system` folder — many commands assume you are in that folder.

Prerequisites
-------------

- A machine with Ubuntu, WSL, or Windows (you will run the appropriate commands
	for your platform)
- Git clone of this repository (or a local copy of the `lto_system` folder)

Step 1: Install Python 3 and venv tools
---------------------------------------

Run on: Ubuntu terminal (or WSL). On Windows, install Python from the official
installer or the Microsoft Store and use the equivalent `python` commands.

Ubuntu / WSL:

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
python3 --version
```

Windows:

- Install Python from https://www.python.org/ or Microsoft Store. Then use
	`python` or `py` in the commands below instead of `python3`.

Step 2: Install MariaDB (if needed)
-----------------------------------

Run on: Ubuntu terminal (or the host where the database will run). If your
database is on another server, perform these steps there or ask your DB admin.

Ubuntu / WSL:

```bash
sudo apt install -y mariadb-server mariadb-client
sudo systemctl enable mariadb
sudo systemctl start mariadb
sudo mysql_secure_installation   # optional but recommended
```

Step 3: Change to the project folder (`lto_system`)
--------------------------------------------------

Before creating the virtualenv or importing SQL, change to the `lto_system`
folder. Use the path that matches your environment.

Windows PowerShell / Command Prompt:

```powershell
d:                      # switch to D: drive if your repo is on D:
cd "D:\UNIBERSIDAD NG PILIPINAS\ACADEMICS\YEAR 4\SEM 7\CMSC 127\LTO System\lto_system"
```

Ubuntu / WSL:

```bash
cd ~/path/to/repo/lto_system
```

Confirm you see `main.py`, `requirements.txt`, and `SQL_Statements.sql`:

```bash
ls
# or on Windows: dir
```

Step 4: Create and activate a virtual environment
-------------------------------------------------

Run inside the `lto_system` folder.

Ubuntu / WSL:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell (from `lto_system`):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Windows Command Prompt (cmd.exe):

```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
```

Step 5: Install Python dependencies (in the venv)
------------------------------------------------

Run inside `lto_system` with the venv active (Ubuntu or Windows shells):

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Step 6: Create database user and import SQL schema + procedures
--------------------------------------------------------------

1) Create DB and user (run in MariaDB shell on the DB host).

Ubuntu / WSL (open MariaDB shell):

```bash
sudo mariadb
```

Inside the MariaDB shell run:

```sql
CREATE DATABASE IF NOT EXISTS lto;
CREATE USER IF NOT EXISTS 'lto_user'@'localhost' IDENTIFIED BY 'lto_password';
GRANT ALL PRIVILEGES ON lto.* TO 'lto_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

2) Import the SQL file (run from the `lto_system` folder where the file is located).

Ubuntu / WSL:

```bash
mariadb -u lto_user -p lto < SQL_Statements.sql
```

Windows PowerShell (if `mariadb` client is installed there):

```powershell
mariadb -u lto_user -p lto < .\SQL_Statements.sql
```

If the DB is remote, include `-h db_host` and ensure the user is allowed to
connect from your client host.

Step 7: Set environment variables for the running session
--------------------------------------------------------

Set these in the same shell where you will run `main.py`.

Ubuntu / WSL (bash):

```bash
export LTO_DB_HOST=localhost
export LTO_DB_PORT=3306
export LTO_DB_USER=lto_user
export LTO_DB_PASSWORD=lto_password
export LTO_DB_NAME=lto
```

Windows PowerShell (temporary for this session):

```powershell
$env:LTO_DB_HOST = 'localhost'
$env:LTO_DB_PORT = '3306'
$env:LTO_DB_USER = 'lto_user'
$env:LTO_DB_PASSWORD = 'lto_password'
$env:LTO_DB_NAME = 'lto'
```

Windows Command Prompt (cmd.exe):

```cmd
set LTO_DB_HOST=localhost
set LTO_DB_PORT=3306
set LTO_DB_USER=lto_user
set LTO_DB_PASSWORD=lto_password
set LTO_DB_NAME=lto
```

Step 8: Run the program
-----------------------

Run in the `lto_system` folder with the venv active and env vars set.

Ubuntu / WSL:

```bash
python3 main.py
```

Windows PowerShell / CMD:

```powershell
python main.py
```

Run Tests (optional)
--------------------

From `lto_system` with venv active:

```bash
pytest
```

Common Issues & Troubleshooting
-------------------------------

- `mariadb: command not found`
	- Install MariaDB on the host: `sudo apt install -y mariadb-server mariadb-client`.

- `Access denied for user`
	- Double-check `LTO_DB_USER`/`LTO_DB_PASSWORD` and that privileges were
		granted from the client host.

- `Unknown database 'lto'`
	- Create it first in the MariaDB shell: `CREATE DATABASE lto;` and re-run import.

- `ModuleNotFoundError` or missing packages
	- Ensure you activated the virtualenv and reinstalled requirements: `pip install -r requirements.txt`.

Notes
-----

- Many controller methods call stored procedures. If the SQL file import
	fails, some features will not work.
- When pushing this repo to GitHub, add a `.gitignore` to exclude `.venv/`,
	`__pycache__/`, and other generated files.

If you want, I can produce a concise `Quick start (Windows)` and `Quick start (Ubuntu)`
section at the top for copy-paste convenience.
