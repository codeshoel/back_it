import os
import datetime
import smtplib
from email.message import EmailMessage
from ftplib import all_errors
from ftplib import FTP
import pandas as pd
from dotenv import dotenv_values
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
from zipfile import ZipFile

# Google drive setup
SCOPE = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'crm-backup-project-1852798251c6.json'
PARENT_FOLDER_ID = "15PEd1WBOJg6L9HsSisurN4DWM6ucVwi1"

def send_email(server, message):
    env = dotenv_values('.env')
    if env:
        email_addr = env.get('EMAIL_ADDR')
        password = env.get('PASSWORD')

        email = EmailMessage()
        email['From'] = email_addr
        email['To'] = email_addr #crmspport@interranetworks.com
        email['Subject'] = 'CRM 64 Backup Report'
        email.set_content(message)

        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(email_addr, password)
            server.send_message(email)
    else:
        print("No variable found in .env file")

def delete_file_older_than(dir, days):
    current_time = datetime.datetime.now()
    cutoff_date = current_time - datetime.timedelta(days=days)
    for root, dirs, files in os.walk(dir):
        for file in files:
            file_path = os.path.join(root, file)
            file_modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_modified_time < cutoff_date:
                print(f"Deleting {file_path} - Last Modified: {file_modified_time}")
                os.remove(file_path)
            else:
                print(f"No file was deleted because no file is older than {cutoff_date}.")

def backup_info(db_name, backup_file_name, *args, **kwargs):
    backup_info = {
        'Database Name': [db_name], 
        'Backed up file name': [backup_file_name],
        'Created at': [datetime.datetime.now()]
    }
    backup_dataframe = pd.DataFrame(data=backup_info)
    database_backup_info_file = os.path.abspath('database_backup_info.csv')
    backup_dataframe.to_csv(database_backup_info_file, mode='a', index=False, header=False)

def authentication():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPE)
    return creds

def upload_backup_to_google_drive(backup_file_name, file_path):
    creds = authentication()
    service = build('drive', 'v3', credentials=creds)
    
    try:
        folder = service.files().get(fileId=PARENT_FOLDER_ID).execute()
        print(f"Folder found: {folder['name']}")
    except Exception as e:
        print(f"Error verifying folder ID: {e}")
        return

    file_metadata = {
        'name': backup_file_name,
        'parents': [PARENT_FOLDER_ID]
    }

    media = MediaFileUpload(file_path, resumable=True)

    try:
        request = service.files().create(body=file_metadata, media_body=media)
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"Uploaded {int(status.progress() * 100)}%.")
        print("Upload Complete.")
    except Exception as e:
        print(f"Error uploading file: {e}")

def backup_database():
    try:
        host = 'localhost'
        user = 'root'
        password = 'wELCOME123'
        database_list = ('ntpmerge', 'campaign', 'carbon', 'carboncrm', 'fairmoneydb', 'ferma', 'health', 'hometown', 'intrustcrm', 'maiguard', 'migo', 'nigsims', 'nphcda', 'ntp', 'ordermgt', 'pollcrm', 'sme', 'yanacrm',)

        for database in database_list:
            backup_file_name = f'{database}-{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.sql'
            os.system(f'mysqldump -h {host} -u {user} -p{password} --no-tablespaces {database} --single-transaction --quick > {backup_file_name}')
            
            zipFile_name = f'{database}-backup-{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.zip'
            
            with ZipFile(f'{zipFile_name}', "w") as newzip:
                newzip.write(backup_file_name)
                os.remove(backup_file_name)
            newzip.close()

            with open(f'{zipFile_name}', "rb") as fp:
                backup_info(database, zipFile_name.replace('.zip', ''))
                upload_backup_to_google_drive(zipFile_name, zipFile_name)

            os.remove(zipFile_name)
        print("Done!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    backup_database()
