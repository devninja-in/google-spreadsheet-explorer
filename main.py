import streamlit as st
from dotenv import load_dotenv
import os
from config import setup_page_config
from components.sidebar import render_sidebar
from components.data_view import render_data_view
from utils.session_state import initialize_session_state

# Load environment variables from .env file
load_dotenv()


def main():
    # Set up page configuration
    setup_page_config()

    # Initialize session state variables
    initialize_session_state()

    # Render sidebar for navigation
    render_sidebar()

    # Render main data view
    if (st.session_state.selected_folder and
            st.session_state.selected_file and
            st.session_state.sheets_data):
        render_data_view()
    else:
        # Instructions when no file is selected
        st.markdown("""
        # Welcome to Google Drive Spreadsheet Explorer

        This app allows you to browse Google Drive folders and view both Google Sheets and Excel files with filtering capabilities.

        ## How to use:

        1. Select a folder from the sidebar
        2. Choose a spreadsheet or Excel file
        3. The app will load all sheets/tabs and display them as tabs in the main area

        ## Features:

        - Browse folders and files in Google Drive
        - View Google Sheets and Excel (.xls/.xlsx) files
        - Display all sheets/tabs simultaneously as tabs
        - Filter data by column values on each tab
        - Search across all columns within each tab
        - Download individual sheets as CSV or Excel
        - Download the entire workbook as an Excel file
        - View summary statistics for numeric data
        """)

    # Add footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("Made with ❤️ with Streamlit")


if __name__ == "__main__":
    main()