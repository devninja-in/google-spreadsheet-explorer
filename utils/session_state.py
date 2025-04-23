import streamlit as st

from config import DEFAULT_BASE_FOLDER_ID


def initialize_session_state():
    """Initialize session state variables if they don't exist"""
    if 'selected_folder' not in st.session_state:
        st.session_state.selected_folder = None
    if 'selected_file' not in st.session_state:
        st.session_state.selected_file = None
    if 'selected_file_type' not in st.session_state:
        st.session_state.selected_file_type = None
    if 'selected_sheet' not in st.session_state:
        st.session_state.selected_sheet = None
    if 'sheets_data' not in st.session_state:
        st.session_state.sheets_data = {}
    if 'sheet_names' not in st.session_state:
        st.session_state.sheet_names = []
    if 'filter_columns' not in st.session_state:
        st.session_state.filter_columns = {}
    if 'file_name' not in st.session_state:
        st.session_state.file_name = ""
    if 'base_folder_id' not in st.session_state:
        # Default to configured base folder ID
        st.session_state.base_folder_id = DEFAULT_BASE_FOLDER_ID