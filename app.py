# import os
# import ftplib
# from ftplib import all_errors
# from ftplib import FTP


# # ftp = FTP('192.168.1.69', user='crm', passwd='wELCOME123', timeout=None)
# # ftp.cwd('back_it')

# # ftp.retrlines('LIST')
# # print("login succeed.")

# # with open('README.md', "rb") as fp:
# #     print(f'file: {fp}')
# #     ftp.storbinary("STOR README.md", fp)
# ftp.quit()
# print('Logged out!')




# Backup datails generation in csv
    # backup_info = {
    #     'database': [database_name], 
    #     'backup_file_name': [backup_file_name],
    #     'created_at': [datetime.datetime.now()]
    #     }
    # backup_dataframe = pd.DataFrame(data=backup_info)

    # Backup details file
    # database_backup_info_file = os.path.abspath('backup.csv')

    # Generate csv file
    # backup_dataframe.to_csv(database_backup_info_file, index=False)

   

    # try:
        

    # except Exception as e:
    #     print(e)




