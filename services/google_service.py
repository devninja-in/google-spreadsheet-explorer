import streamlit as st
import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build


@st.cache_resource
def get_google_services():
    """
    Authenticate with Google Drive & Sheets APIs
    Returns a tuple of (drive_service, sheets_service)
    """
    try:
        # For deployment, you can use st.secrets
        service_account_info = st.secrets["google_credentials"]
    except:
        # For local development
        try:
            service_account_info = json.loads(os.environ['GOOGLE_DRIVE_CREDENTIALS'])
        except:
            # Fallback to GOOGLE_CREDENTIALS environment variable
            service_account_info = eval(os.environ.get("GOOGLE_CREDENTIALS", "{}"))

    if not service_account_info:
        st.error("Google credentials not found! Please set up service account credentials.")
        st.stop()

    credentials = service_account.Credentials.from_service_account_info(
        service_account_info,
        scopes=[
            'https://www.googleapis.com/auth/drive.readonly',
            'https://www.googleapis.com/auth/spreadsheets.readonly'
        ]
    )

    drive_service = build('drive', 'v3', cache_discovery=False, credentials=credentials)
    sheets_service = build('sheets', 'v4', cache_discovery=False, credentials=credentials)

    return drive_service, sheets_service


def list_folders(drive_service, parent_folder_id):
    print("Listing folders from {}".format(parent_folder_id))
    folders = drive_service.files().list()
    """List all folders within a parent folder"""
    query = f"'{parent_folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and trashed=false"

    response = drive_service.files().list(
        q=query,
        spaces='drive',
        supportsAllDrives=True,
        includeItemsFromAllDrives=True,
        fields='files(id, name)',
        orderBy='name'
    ).execute()

    folders = response.get('files', [])
    return folders


def list_files(drive_service, folder_id):
    """List all spreadsheet files in a folder"""
    print(f'Listing files in folder {folder_id}')
    query = f"'{folder_id}' in parents and (mimeType='application/vnd.google-apps.spreadsheet' or mimeType='application/vnd.ms-excel' or mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') and trashed=false"

    response = drive_service.files().list(
        q=query,
        spaces='drive',
        supportsAllDrives=True,
        includeItemsFromAllDrives=True,
        fields='files(id, name, mimeType)',
        orderBy='name'
    ).execute()

    files = response.get('files', [])
    return files


def get_spreadsheet_metadata(sheets_service, spreadsheet_id):
    """Get metadata for a Google spreadsheet (sheet names)"""
    spreadsheet = sheets_service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheets = spreadsheet.get('sheets', [])
    sheet_names = [sheet['properties']['title'] for sheet in sheets]
    file_title = spreadsheet['properties']['title']
    return sheet_names, file_title


def get_sheet_data(sheets_service, spreadsheet_id, sheet_name):
    """Read data from a specific sheet in a Google spreadsheet"""
    print(f'Getting data from {sheet_name}')
    range_name = f"'{sheet_name}'"
    result = sheets_service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])

    return values


def get_file_details(drive_service, file_id):
    """Get file details for a specific file"""
    return drive_service.files().get(
        fileId=file_id,
        supportsAllDrives=True,
        fields="name"
    ).execute()