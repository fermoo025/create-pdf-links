from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request
import os, io, time
from datetime import datetime
import requests
import csv

now = datetime.now().strftime('%y-%m-%d %H%M%S')
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
FOLDER_ID = '1c6l8cZRLqtbeyyvKlp9Nm2xOJHNkaDBf'  # ⬅️ Replace this with your folder ID
SHEET_ID= '1CVAAilMvM8LsrZIelRz6nf4SRvFeoawGonw6L4QlSC8'

def authenticate():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def download_pdfs_from_folder(service, folder_id):
    if os.path.exists(folder_id):
        return
    query = f"'{folder_id}' in parents and mimeType='application/pdf'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])

    if not files:
        print("No PDF files found in the folder.")
        return
    pdfDir= f"pdfs {now}"
    os.makedirs(pdfDir);
    for file in files:
        print(f"Downloading: {file['name']}")
        request = service.files().get_media(fileId=file['id'])
        fh = io.FileIO(f"{pdfDir}/{file['name']}", 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"  Progress: {int(status.progress() * 100)}%")
    print("✅ Finished downloading all PDFs from the folder.")

def download_sheet_as_xlsx(service, file_id, filename):
    request = service.files().export_media(
        fileId=file_id,
        mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    fh = io.FileIO(filename, 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Downloaded {filename}: {int(status.progress() * 100)}%")

def download_sheet_as_csv(service, spreadsheet_id, sheet_name, file_name):
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=sheet_name).execute()
    values = result.get('values', [])
    if not values:
        print('No data found.')
        return 0
    with open(file_name, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerows(values)
    return 1

def main(folderId, sheetId, tabName):
    tic=time.time()
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)
    download_pdfs_from_folder(service, folderId)
    service = build('sheets', 'v4', credentials=creds)
    download_sheet_as_csv(service, sheetId, tabName, f'{tabName}.csv')
    print(time.time()-tic);
if __name__ == '__main__':
    main()
