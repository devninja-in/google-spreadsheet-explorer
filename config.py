import os

import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Default base folder ID from environment variables
DEFAULT_BASE_FOLDER_ID = os.environ.get('GOOGLE_DRIVE_PARENT_FOLDER_ID')


def setup_page_config():
    """Configure the Streamlit page settings"""
    st.set_page_config(
        page_title="Google Sheets Explorer",
        page_icon="📊",
        layout="wide"
    )
