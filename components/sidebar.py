import streamlit as st
from services.google_service import get_google_services, list_folders, list_files, get_spreadsheet_metadata
from utils.file_operations import download_excel_file, read_excel_sheets, create_download_excel
from utils.data_processing import get_all_sheets_data
import io


def render_sidebar():
    """Render the sidebar navigation component"""
    with st.sidebar:
        st.header("Navigation")

        try:
            # Get Google services
            drive_service, sheets_service = get_google_services()

            # List folders
            folders = list_folders(drive_service, st.session_state.base_folder_id)

            folder_names = [folder['name'] for folder in folders]
            folder_ids = [folder['id'] for folder in folders]

            st.subheader("Select Folder")
            selected_folder_index = st.selectbox(
                "Choose a folder",
                options=range(len(folder_names)),
                format_func=lambda x: folder_names[x],
                index=0 if folder_names else None
            )

            if selected_folder_index is not None and folder_ids:
                selected_folder_id = folder_ids[selected_folder_index]
                if st.session_state.selected_folder != selected_folder_id:
                    st.session_state.selected_folder = selected_folder_id
                    st.session_state.selected_file = None
                    st.session_state.selected_file_type = None
                    st.session_state.selected_sheet = None
                    st.session_state.sheets_data = {}
                    st.session_state.sheet_names = []
                    st.session_state.filter_columns = {}
                    st.session_state.file_name = ""
                    st.rerun()

            # If folder is selected, list files
            if st.session_state.selected_folder:
                files = list_files(drive_service, st.session_state.selected_folder)

                file_names = [file['name'] for file in files]
                file_ids = [file['id'] for file in files]
                file_types = [file['mimeType'] for file in files]

                st.subheader("Select Spreadsheet")
                selected_file_index = st.selectbox(
                    "Choose a file",
                    options=range(len(file_names)),
                    format_func=lambda x: file_names[x],
                    index=0 if file_names else None
                )

                if selected_file_index is not None and file_ids:
                    selected_file_id = file_ids[selected_file_index]
                    selected_file_type = file_types[selected_file_index]
                    selected_file_name = file_names[selected_file_index]

                    if (st.session_state.selected_file != selected_file_id or
                            st.session_state.selected_file_type != selected_file_type):
                        st.session_state.selected_file = selected_file_id
                        st.session_state.selected_file_type = selected_file_type
                        st.session_state.selected_sheet = None
                        st.session_state.sheets_data = {}
                        st.session_state.sheet_names = []
                        st.session_state.filter_columns = {}
                        st.session_state.file_name = selected_file_name
                        st.rerun()

                # If file is selected, load sheet data
                if st.session_state.selected_file and st.session_state.selected_file_type:
                    # Load data if not already loaded
                    if not st.session_state.sheets_data:
                        with st.spinner("Loading spreadsheet data..."):
                            if st.session_state.selected_file_type == 'application/vnd.google-apps.spreadsheet':
                                # Google Sheets
                                sheet_names, file_title = get_spreadsheet_metadata(sheets_service,
                                                                                   st.session_state.selected_file)
                                sheets_data = get_all_sheets_data(sheets_service, st.session_state.selected_file,
                                                                  sheet_names)
                                st.session_state.sheet_names = sheet_names
                                st.session_state.sheets_data = sheets_data
                                st.session_state.file_name = file_title
                            else:
                                # Excel file
                                excel_buffer = download_excel_file(drive_service, st.session_state.selected_file)
                                sheets_data, sheet_names = read_excel_sheets(excel_buffer)
                                st.session_state.sheet_names = sheet_names
                                st.session_state.sheets_data = sheets_data

                    # Download entire spreadsheet button
                    if st.button("Download Entire Spreadsheet"):
                        if st.session_state.selected_file_type == 'application/vnd.google-apps.spreadsheet':
                            # For Google Sheets, export as Excel
                            with st.spinner("Preparing download..."):
                                output = create_download_excel(st.session_state.sheets_data, st.session_state.file_name)

                                st.download_button(
                                    label="Download Excel File",
                                    data=output,
                                    file_name=f"{st.session_state.file_name}.xlsx",
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                )
                        else:
                            # For Excel files, just download the original
                            with st.spinner("Preparing download..."):
                                excel_buffer = download_excel_file(drive_service, st.session_state.selected_file)
                                st.download_button(
                                    label="Download Excel File",
                                    data=excel_buffer,
                                    file_name=st.session_state.file_name,
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                                )
        except Exception as e:
            st.error(f"Error connecting to Google Drive API: {str(e)}")