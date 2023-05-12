import os
import datetime
from ftplib import all_errors
from ftplib import FTP
import pandas as pd


# Create database backup
host = 'localhost'
user = 'root'
password = 'wELCOME123'; #
database_name = 'new_carbon'
backup_file_name = f'{database_name}-{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.sql'


def backup_info(db_name, backup_file_name, *args, **kwargs):
    # Backup datails generation in csv
    backup_info = {
        'Database Name': [db_name], 
        'Backed up file name': [backup_file_name],
        'Created at': [datetime.datetime.now()]
        }
    backup_dataframe = pd.DataFrame(data=backup_info)

    # Backup details file
    database_backup_info_file = os.path.abspath('database_backup_info.csv')

    # Generate csv file
    backup_dataframe.to_csv(database_backup_info_file, mode='a', index=False, header=False)


def backup_database():

    # Initiate server connection(i.e your remote server)
    ftp = FTP('192.168.1.69', user='crm', passwd='wELCOME123', timeout=None)

    # server directory where you want to upload file to.
    ftp.cwd('back_it/66')

    ftp.retrlines('LIST')
    print("login succeed.")

    try:
        # if you want all the database on the server replace database name with --all-databases cmd
        # -h: server, -u: user, -p: password(ensure your -p&yourpassword are written in one word(e.g -p123456))
        os.system(f'mysqldump -h {host} -u {user} -p{password} --no-tablespaces {database_name} --single-transaction --quick > {backup_file_name}')
        
        # File to be backed up on the cloud
        # open(filename, rb)
        with open(f'{backup_file_name}', "rb") as fp:
            
            # Transfer backed up file to remote server.
            ftp.storbinary(f"STOR {backup_file_name}", fp)
            backup_info(database_name, backup_file_name)

        # Close the file after reading from it.
        fp.close()

        # Remove backup file after successfully uploading file to server.
        os.remove(backup_file_name)
        print("Done!")


        
    except all_errors as xe:
        print(xe)

    finally:
        # logout
        ftp.quit()


if __name__ == '__main__':
    backup_database()


















