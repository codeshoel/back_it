import os
import datetime
import smtplib
from email.message import EmailMessage
from ftplib import all_errors
from ftplib import FTP
import pandas as pd
from dotenv import dotenv_values


# from googleapiclient.discovery import build
# from google.oauth2 import service_account

# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive

from zipfile import ZipFile


# Google drive setup
SCOPE = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE='crm-backup-project-1852798251c6.json'
PARENT_FOLDER_ID="15PEd1WBOJg6L9HsSisurN4DWM6ucVwi1"



def send_email(server, message):
    # initialize env
    env = dotenv_values('.env')
    
    # Access env variables
    if env:
        email_addr = env.get('EMAIL_ADDR')
        password = env.get('PASSWORD')
        
        # Email content
        email = EmailMessage()
        email['From'] = email_addr
        email['To'] = email_addr
        email['Subject'] = '9psb Backup Detail'

        email.set_content(message)

        # Establish connection to SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()  # Enable TLS encryption
            server.login(email_addr, password)  # Use app password if 2-step verification is enabled
            server.send_message(email)
    else:
        print("No variable found in .env file")

def delete_file_older_than(dir, days):
    # Get current time
    current_time = datetime.datetime.now()

    # Calculate cutoff date based on the number of days
    cutoff_date = current_time - datetime.timedelta(days=days)

    # Loop through the files in the directory
    for root, dirs, files in os.walk(dir):
        for file in files:
            file_path = os.path.join(root, dir)
            file_modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))

            # Check if the file's modification time is older than the cutoff date
            if file_modified_time < cutoff_date:
                print(f"Deleting {file_path} - Last Modified: {file_modified_time}")

                # Remove file(s)
                os.remove(file_path)
            else:
                print(f"No file was deleted because no file is older than {cutoff_date}.")


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


def authentication():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
    return creds


def upload_backup_to_google_drive(backup_file_name, file_path):
    creds = authentication()
    service = build('drive', 'v3', credentials=creds)
    file_metadata = {
        'name': backup_file_name,
        'parents': [PARENT_FOLDER_ID]
    }

    _file = service.files().create(
        body=file_metadata,
        media_body=file_path
    ).execute()




# def backup_to_google_drive(backup_file_name, file_path):
#     gauth = GoogleAuth()
#     gauth.LocalWebserverAuth() # Create local webserver and auto handle authentication.

#     # Authenticate user 
#     drive = GoogleDrive(gauth)

#     # folder credential
#     # folderId: https://drive.google.com/drive/folders/1rJFUBbi3FYm_qUW2vsexLTOe25bTQ3K2
#     folder = '1s3QN1PLCKDCWmT0ICgG-CW8_02W7qkwb'


#     file1 = drive.CreateFile({"parents": [{'id': folder}], 'title': backup_file_name}) # Create GoogleDriveFile instance with title 'Hello.txt'.
#     file1.SetContentFile(file_path) # Set content of the file from given string.
#     file1.Upload()


def backup_database():
    # server_IP = '192.168.1.69'
    try:
        # Initiate server connection(i.e your remote server)
        # ftp = FTP(server_IP, user='crm', passwd='wELCOME123', timeout=None)

        # # server directory where you want to upload file to.
        # ftp.cwd('back_it/test_dir')

        # ftp.retrlines('LIST')
        # print("login succeed.")

        try:
            # Create database backup
            host = 'localhost'
            user = 'root'
            password = '';
            database_list = ('nigsims_db',)

            # Zip file name
            zipFile_name = f'backup-{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.zip'


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
                # ftp.storbinary(f"STOR {zipFile_name}", fp)

                # backup_file_name = zipFile_name.replace('.zip', '')
                # print(backup_file_name)
                
                # Information about the backup
                backup_info(database, zipFile_name.replace('.zip', ''))

                # backup to Google drive
                upload_backup_to_google_drive(zipFile_name, zipFile_name)

            # Close the file after reading from it.
            fp.close()

            # Remove backup file after successfully uploading file to server.
            os.remove(zipFile_name)
            print("Done!")

        except all_errors as xe:
            print(xe)

        finally:
            pass
            # logout
            # ftp.quit()
    except all_errors as ex:
        print(f'ftpError: {ex}')


if __name__ == '__main__':
    # this function is for backup
    backup_database()

    # delete files older than specified period
    day=1
    month=30
    year=365
    # delete_file_older_than()

