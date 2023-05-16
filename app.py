import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# database_backup (folder name)
# folderId: https://drive.google.com/drive/folders/1rJFUBbi3FYm_qUW2vsexLTOe25bTQ3K2



gauth = GoogleAuth()
gauth.LocalWebserverAuth() # Create local webserver and auto handle authentication.


drive = GoogleDrive(gauth)

folder = '1rJFUBbi3FYm_qUW2vsexLTOe25bTQ3K2'


file1 = drive.CreateFile({"title": [{'id': folder}], 'title': 'hello.txt'}) # Create GoogleDriveFile instance with title 'Hello.txt'.
file1.SetContentString('Hello world!') # Set content of the file from given string.
file1.Upload()




