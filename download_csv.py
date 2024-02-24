import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.credentials import Credentials
import json

SCOPES = ['https://www.googleapis.com/auth/drive']

script_dir = os.path.dirname(os.path.realpath(__file__))

# token_path = os.path.join(script_dir, "token.json")
# creds = Credentials.from_authorized_user_file("token.json", SCOPES)
# SERVICE_ACCOUNT_FILE = 'token.json'

token_data = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

# Load token data as JSON
creds = Credentials.from_authorized_user_info(json.loads(token_data))
SERVICE_ACCOUNT_FILE = token_data 

KEYWORD = 'Attendance report'
DOWNLOAD_FOLDER = 'down'

drive_service = build('drive', 'v3', credentials=creds)

# Check if the download folder exists, if not, create it
download_folder_path = os.path.join(script_dir, DOWNLOAD_FOLDER)
if not os.path.exists(download_folder_path):
    os.makedirs(download_folder_path)

results = drive_service.files().list(
    q=f"name contains '{KEYWORD}' and mimeType = 'application/vnd.google-apps.spreadsheet'",
    fields="files(id, name)"
).execute()

# Download each file found with the keyword
if 'files' in results and len(results['files']) > 0:
    for file in results['files']:
        file_id = file['id']
        file_name = file['name']

        # Export the file to CSV
        request = drive_service.files().export_media(fileId=file_id,
                                                     mimeType='text/csv')
        file_path = os.path.join(download_folder_path, file_name + '.csv')
        file_stream = open(file_path, 'wb')
        downloader = MediaIoBaseDownload(file_stream, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
        file_stream.close()

        print(f"File '{file_name}.csv' exported and downloaded successfully.")
else:
    print("No files found with the given keyword.")
