# import pyodbc
# import os
# import mysql.connector
# import datetime
# import ftplib


# # Connection properties declaration
# server      =   'localhost' # Server name, can be 127.0.0.1
# username    =   'root'      # Database username
# password    =   ''          # Database password
# database    =   'g-store'# Database name
# port        =   3306

# conn = mysql.connector.connect(host=server, user=username, password=password, database=database)
# db = conn.cursor()

# backup_dir = 'C:/Users/KEN/Downloads'

# # backup file name
# backup_file = 'backup_file_'+str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')) +'.sql'

# file_location = os.path.join(backup_dir, backup_file)
# print(file_location)

# # backup command
# backup_command = 'BACKUP DATABASE g-store TO DISK =%s'.format(file_location)

# query = 'SELECT * FROM store_category'


# # Execute backup command
# db.execute(backup_command)
# # for i in db:
# #     print(i)
# print("Done !")










# # if __name__ == '__main__':
# #     app = BackIt();
# #     app.run()