import os
import datetime
from ftplib import all_errors
from ftplib import FTP
import pandas as pd

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


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


# def backup_to_google_drive(backup_file_name, file_path):
#     gauth = GoogleAuth()
#     gauth.LocalWebserverAuth() # Create local webserver and auto handle authentication.

    # Authenticate user 
    # drive = GoogleDrive(gauth)

    # folder credential
    # folderId: https://drive.google.com/drive/folders/1rJFUBbi3FYm_qUW2vsexLTOe25bTQ3K2
    # folder = '1s3QN1PLCKDCWmT0ICgG-CW8_02W7qkwb'


    # file1 = drive.CreateFile({"parents": [{'id': folder}], 'title': backup_file_name}) # Create GoogleDriveFile instance with title 'Hello.txt'.
    # file1.SetContentFile(file_path) # Set content of the file from given string.
    # file1.Upload()


def backup_database():

    # Initiate server connection(i.e your remote server)
    ftp = FTP('***', user='crm', passwd='***', timeout=None)

    # server directory where you want to upload file to.
    ftp.cwd('back_it/dir')

        ftp.retrlines('LIST')
        print("login succeed.")

        try:
            # Create database backup
            host = 'localhost'
            user = 'root'
            password = '123456';
            database_list = ('g-store', 'ticketing_system')
            # backup_file_name = f'{database_list}-{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.sql'

            # if you want all the database on the server replace database name with --all-databases cmd
            # -h: server, -u: user, -p: password(ensure your -p&yourpassword are written in one word(e.g -p123456))
            for database in database_list:
                backup_file_name = f'{database}-{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.sql'
                os.system(f'mysqldump -h {host} -u {user} -p{password} --no-tablespaces {database} --single-transaction --quick > {backup_file_name}')


            # list all .sql file in parant dir and compress to zip file
            file_in_dir = os.listdir()
            with ZipFile(f'{zipFile_name}', "w") as newzip:
                for file in file_in_dir:
                    if file.endswith('.sql'):
                        newzip.write(file)

                        # Remove file after 
                        os.remove(file)
            newzip.close()



            # File to be backed up on the cloud
            with open(f'{zipFile_name}', "rb") as fp:
                # backup to remote server.
                ftp.storbinary(f"STOR {zipFile_name}", fp)
                
                # Information about the backup
                backup_info(database, zipFile_name.replace('.zip', ''))

                # backup to Google drive
                # backup_to_google_drive(backup_file_name, backup_file_name)

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
    except all_errors as ex:
        print(f'ftpError: {ex}')


if __name__ == '__main__':
    backup_database()


















