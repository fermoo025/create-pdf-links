from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import io
from googleapiclient.http import MediaIoBaseDownload

# If modifying these SCOPES, delete token.json
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

def main():
    creds = None

    # Load token if it exists
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # Authenticate if no token
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save token for later runs
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Build the Drive service
    service = build('drive', 'v3', credentials=creds)

    # Replace with your file ID
    file_id = '1shT7RkNhYDga0rpyx8vf4uZfEu24qPq8'
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO('downloaded_file.pdf', 'wb')
    downloader = MediaIoBaseDownload(fh, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f'Download progress: {int(status.progress() * 100)}%')

if __name__ == '__main__':
    import os
    from google.auth.transport.requests import Request
    main()
