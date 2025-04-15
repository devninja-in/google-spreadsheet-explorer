import io
import pandas as pd
from googleapiclient.http import MediaIoBaseDownload
import streamlit as st


def download_excel_file(drive_service, file_id):
    """Download Excel file from Google Drive"""
    request = drive_service.files().get_media(fileId=file_id)
    file_buffer = io.BytesIO()
    downloader = MediaIoBaseDownload(file_buffer, request)

    done = False
    while not done:
        status, done = downloader.next_chunk()

    file_buffer.seek(0)
    return file_buffer


def read_excel_sheets(excel_buffer):
    """Read all sheets from Excel file"""
    # Read all sheets into a dict of dataframes
    excel_file = pd.ExcelFile(excel_buffer)
    sheet_names = excel_file.sheet_names

    sheets_data = {}
    for sheet_name in sheet_names:
        df = pd.read_excel(excel_file, sheet_name=sheet_name)
        sheets_data[sheet_name] = df

    return sheets_data, sheet_names


def create_download_excel(sheets_data, file_name):
    """Create Excel file for download with multiple sheets"""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        for sheet_name, df in sheets_data.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    output.seek(0)

    return output


def create_download_csv(df, file_name, sheet_name):
    """Create CSV file for download"""
    csv = df.to_csv(index=False).encode('utf-8')
    return csv


def create_download_sheet_excel(df, file_name, sheet_name):
    """Create Excel file for download with a single sheet"""
    buffer = io.BytesIO()
    df.to_excel(buffer, index=False)
    buffer.seek(0)
    return buffer