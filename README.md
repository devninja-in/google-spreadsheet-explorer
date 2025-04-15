# Google Drive Spreadsheet Explorer

A Streamlit application for browsing and analyzing Google Drive spreadsheets and Excel files.

## Project Structure

```
.
├── main.py                     # Application entry point
├── config.py                   # Configuration settings
├── components/                 # UI components
│   ├── sidebar.py              # Sidebar navigation
│   └── data_view.py            # Data display components
├── services/                   # External API services
│   └── google_service.py       # Google Drive/Sheets API
├── utils/                      # Utility functions
│   ├── file_operations.py      # File handling utilities
│   ├── data_processing.py      # Data processing utilities
│   └── session_state.py        # Streamlit session state management
├── .env                        # Environment variables (not tracked in Git)
└── requirements.txt            # Project dependencies
```

## Features

- Browse folders and files in Google Drive
- View Google Sheets and Excel (.xls/.xlsx) files
- Display all sheets/tabs simultaneously as tabs
- Filter data by column values on each tab
- Search across all columns within each tab
- Download individual sheets as CSV or Excel
- Download the entire workbook as an Excel file
- View summary statistics for numeric data

## Setup

1. Create a Google Cloud Project and enable the Google Drive and Google Sheets APIs
2. Create a service account and download the JSON credentials
3. Create a `.env` file with the following environment variables:
   ```
   GOOGLE_DRIVE_CREDENTIALS='{"type": "service_account", ...}'
   GOOGLE_DRIVE_PARENT_FOLDER_ID='your_folder_id'
   ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
5. Run the application:
   ```
   streamlit run main.py
   ```

## Environment Variables

- `GOOGLE_DRIVE_CREDENTIALS`: JSON string of Google service account credentials
- `GOOGLE_DRIVE_PARENT_FOLDER_ID`: The ID of the parent folder to browse (optional, defaults to root)

## Podman Steps
- podman build -t google-spreadsheet-explorer .
- podman run --env-file .env -p 8501:8501 google-spreadsheet-explorer
