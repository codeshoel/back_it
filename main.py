from email.mime.text import MIMEText
import os
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import pandas as pd
from dotenv import dotenv_values
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload
from zipfile import ZipFile

env = dotenv_values('.env')

# Google drive setup
SCOPE = env.get('SCOPE').split(',')
SERVICE_ACCOUNT_FILE = env.get('SERVICE_ACCOUNT_FILE')
PARENT_FOLDER_ID = env.get('PARENT_FOLDER_ID')
FULL_BACKUP_FOLDER_ID = env.get('FULL_BACKUP_FOLDER_ID')
INCREMENTAL_BACKUP_FOLDER_ID = env.get('INCREMENTAL_BACKUP_FOLDER_ID')
BACKUP_LOG_FILE = env.get('BACKUP_LOG_FILE')
BACKUP_TYPE = int(env.get('BACKUP_TYPE'))

def send_email_with_log(message):
    if env:
        email_addr = env.get('EMAIL_ADDR')
        password = env.get('PASSWORD')

        email = MIMEMultipart()
        email['From'] = email_addr
        email['To'] = email_addr
        email['Subject'] = 'CRM 64 Backup Report'
        email.attach(MIMEText(message, 'plain'))

        with open(BACKUP_LOG_FILE, "rb") as f:
            attach = MIMEApplication(f.read(), _subtype="csv")
            attach.add_header('Content-Disposition', 'attachment', filename=BACKUP_LOG_FILE)
            email.attach(attach)

        with smtplib.SMTP(env.get('DOMAIN'), env.get('OUTGOING_PORT')) as server:
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

def backup_info(db_name, backup_file_name, start_time, end_time, last_operation):
    backup_info = {
        'name': [backup_file_name],
        'start datetime': [start_time],
        'end datetime': [end_time],
        'last operation': [last_operation]
    }
    backup_dataframe = pd.DataFrame(data=backup_info)
    if not os.path.exists(BACKUP_LOG_FILE):
        backup_dataframe.to_csv(BACKUP_LOG_FILE, mode='w', index=False)
    else:
        backup_dataframe.to_csv(BACKUP_LOG_FILE, mode='a', index=False, header=False)

def authentication():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPE)
    return creds

def upload_backup_to_google_drive(backup_file_name, file_path):
    creds = authentication()
    service = build('drive', 'v3', credentials=creds)
    
    try:
        _folder = FULL_BACKUP_FOLDER_ID if BACKUP_TYPE == 0 else INCREMENTAL_BACKUP_FOLDER_ID
        folder = service.files().get(fileId=_folder).execute()
        print(f"Folder found: {folder['name']}")
    except Exception as e:
        print(f"Error verifying folder ID: {e}")
        return

    file_metadata = {
        'name': backup_file_name,
        'parents': [_folder]
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

def get_last_backup_time():
    if os.path.exists(BACKUP_LOG_FILE):
        df = pd.read_csv(BACKUP_LOG_FILE)
        last_backup = df['end datetime'].max()
        return datetime.datetime.strptime(last_backup, '%Y-%m-%d %H:%M:%S')
    return None

def backup_database():
    try:
        host = env.get('HOST')
        user = env.get('USER')
        password = env.get('PASSWORD')
        database_list = ('campaign', 'carbon', 'carboncrm', 'fairmoneydb', 'ferma', 'health', 'hometown', 'intrustcrm', 'maiguard', 'migo', 'nigsims', 'nphcda', 'ntp', 'ordermgt', 'pollcrm', 'sme', 'yanacrm',)
        port=env.get('PORT')

        last_backup_time = get_last_backup_time()
        current_time = datetime.datetime.now()
        
        all_backups_successful = True
        backup_message = ""

        for database in database_list:
            start_time = datetime.datetime.now()
            
            if last_backup_time:
                # Incremental backup since last backup
                backup_file_name = f'{database}-incremental-{current_time.strftime("%Y-%m-%d_%H-%M-%S")}.sql'
                # os.system(f'mysqldump -h {host} -u {user} -p{password} --no-tablespaces {database} --single-transaction --quick --where="timestamp > \'{last_backup_time.strftime("%Y-%m-%d %H:%M:%S")}\'" > {backup_file_name}')
                os.system(f'mysqldump -h {host} -P {port} -u {user} -p{password} --no-tablespaces {database} --single-transaction --quick --where="timestamp > \'{last_backup_time.strftime("%Y-%m-%d %H:%M:%S")}\'" > {backup_file_name}')

                last_operation = 'incremental'
                BACKUP_TYPE = 1
            else:
                # Full backup
                backup_file_name = f'{database}-full-{current_time.strftime("%Y-%m-%d_%H-%M-%S")}.sql'
                os.system(f'mysqldump -h {host} -P {port} -u {user} -p{password} --no-tablespaces {database} --single-transaction --quick > {backup_file_name}')
                last_operation = 'full'
                BACKUP_TYPE = 0
            
            zipFile_name = f'{database}-backup-{current_time.strftime("%Y-%m-%d_%H-%M-%S")}.zip'
            
            try:
                with ZipFile(f'{zipFile_name}', "w") as newzip:
                    newzip.write(backup_file_name)
                    os.remove(backup_file_name)
                newzip.close()

                backup_info(database, zipFile_name.replace('.zip', ''), start_time, datetime.datetime.now(), last_operation)
                upload_backup_to_google_drive(zipFile_name, zipFile_name)

                os.remove(zipFile_name)
            except Exception as e:
                all_backups_successful = False
                backup_message += f"Error backing up database {database}: {e}\n"

        if all_backups_successful:
            backup_message += "All databases backed up successfully."
            send_email_with_log(backup_message)

        print("Done!")

    except Exception as e:
        print(f"Error: {e}")
        send_email_with_log(f"Backup process encountered an error: {e}")

if __name__ == '__main__':
    backup_database()
