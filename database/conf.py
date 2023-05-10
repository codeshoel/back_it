import pyodbc

# Connection properties declaration
server      =   'localhost' # Server name, can be 127.0.0.1
username    =   'root'      # Database username
password    =   ''          # Database password
database    =   'g-store'   # Database name


class DBConnection:

    def cursor(self):
        try:
            db_conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
            cursor = db_conn.cursor()
            True
        except Exception as e:
            print(e)
            False









