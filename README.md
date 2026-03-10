# BackIt
This project provides a solution to database backing up, making database backup seamless to drive productivity.

## Features
-   Backup single and multiple databases
-   Transfer the backed-up database to a remote server.
-   Generate a report for the backup database in CSV format.

### Installation
To install and run BackIt, follow these installation guides:
1. Clone the repository:
```bash git clone https://github.com/codeshoel/back_it.git```
2. Install dependencies:
```bash pip install -r requirements.txt```
3. Add mysqldump to the system environment
## On Windows
-   For Xampp server
    ```C:\xampp\mysql\bin```
-   For Wamp64 server
    ```C:\wamp64\bin\mysql\mysql5.7.31\bin```
## Run script with:
```bash py main.py```

# Food for thought:
-   Make sure the database is passworded if you intend to run with Task Scheduler.


## Potential Error and How to Fix:

- If faced with package installation error: 
    - ``pip._vendor.pyproject_hooks._impl.BackendUnavailable: Cannot import 'setuptools.build_meta``

    - ```bash python.exe -m pip install --upgrade pip setuptools wheel ```

# OR

- Run:
    - ```bash python.exe -m pip install --force-reinstall pip setuptools wheel ```

- Reinstall the packages:
    - ```bash python.exe -m pip install -r requirements.txt ```

# Add the following environment variables in your .env
``` # EMAIL CONFIGURATION SETTINGS
DOMAIN=
INCOMING_PORT=
OUTGOING_PORT=
ENABLE=ssl


# EMAIL CREDENTIALS
EMAIL_ADDR=
PASSWORD=

#Google Drive Settings
SCOPE = 
SERVICE_ACCOUNT_FILE = 
PARENT_FOLDER_ID = 
FULL_BACKUP_FOLDER_ID = 
INCREMENTAL_BACKUP_FOLDER_ID = 
BACKUP_LOG_FILE = 'backup_log.csv'
BACKUP_TYPE = 0

# Database Settings
HOST=localhost
PORT=
USER=
PASSWORD= ```