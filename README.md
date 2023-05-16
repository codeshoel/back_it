# BackIt
BackIt is a project that provides solution to database backing up, making database backup seamless to drive productivity.

## Features
-   Backup single and multiple database
-   Transfer backed up database to remote server.
-   Generate report for backup database in csv format.

### Installation
To install and run BackIt, follow these installation guid:
1. Clone the repository:
```bash git clone https://github.com/codeshoel/back_it.git```
2. Install dependencies:
```bash pip install -r requirements.txt```
3. Add mysqldump to system environment
## On Windows
-   For Xampp server
    ```C:\xampp\mysql\bin```
-   For Wamp64 server
    ```C:\wamp64\bin\mysql\mysql5.7.31\bin```
## Run script with:
```bash py main.py```

# Food for thought:
-   Make sure the database is passworded if you enttend running with Task Scheduler.






