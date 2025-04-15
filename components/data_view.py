import streamlit as st
import pandas as pd
from services.google_service import get_google_services, get_file_details
from utils.data_processing import apply_filters, apply_search, get_numeric_stats
from utils.file_operations import create_download_csv, create_download_sheet_excel

def render_data_sheet(sheet_name, df):
    """Render the data view for a single sheet"""
    if df.empty:
        st.warning(f"No data found in sheet: {sheet_name}")
        return

    # Display data summary
    st.subheader("Data Overview")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"Number of rows: {len(df)}")
    with col2:
        st.write(f"Number of columns: {len(df.columns)}")

    # Filters - using session state with sheet-specific keys
    filter_key = f"filter_{sheet_name}"
    if filter_key not in st.session_state:
        st.session_state[filter_key] = {}

    st.subheader("Filters")

    filter_container = st.container()

    with filter_container:
        col1, col2, col3 = st.columns(3)

        with col1:
            filter_column = st.selectbox(
                "Select column to filter",
                options=['None'] + list(df.columns),
                key=f"filter_column_{sheet_name}"
            )

        if filter_column != 'None':
            with col2:
                unique_values = df[filter_column].dropna().unique()
                if len(unique_values) > 0 and len(unique_values) <= 30:
                    # Only offer multi-select for reasonable number of options
                    filter_values = st.multiselect(
                        "Select values",
                        options=sorted(unique_values),
                        default=list(unique_values),
                        key=f"filter_values_{sheet_name}_{filter_column}"
                    )
                    if filter_values:
                        st.session_state[filter_key][filter_column] = filter_values
                    elif filter_column in st.session_state[filter_key]:
                        del st.session_state[filter_key][filter_column]
                else:
                    filter_text = st.text_input(
                        f"Filter text for {filter_column}",
                        key=f"filter_text_{sheet_name}_{filter_column}"
                    )
                    if filter_text:
                        st.session_state[filter_key][filter_column] = filter_text
                    elif filter_column in st.session_state[filter_key]:
                        del st.session_state[filter_key][filter_column]

        with col3:
            if st.session_state[filter_key]:
                if st.button("Clear All Filters", key=f"clear_filters_{sheet_name}"):
                    st.session_state[filter_key] = {}
                    st.rerun()

    # Display active filters
    if st.session_state[filter_key]:
        st.subheader("Active Filters")
        for col, values in st.session_state[filter_key].items():
            if isinstance(values, list):
                st.write(f"- **{col}**: {', '.join(map(str, values))}")
            else:
                st.write(f"- **{col}**: contains '{values}'")

    # Apply filters to dataframe
    filtered_df = apply_filters(df, st.session_state[filter_key])

    # Display data
    st.subheader(f"Data from {sheet_name}")

    # Add search functionality
    search_term = st.text_input("Search across all columns", "", key=f"search_{sheet_name}")
    if search_term:
        filtered_df = apply_search(filtered_df, search_term)

    # Select columns to display
    all_columns = list(filtered_df.columns)
    selected_columns = st.multiselect(
        "Select columns to display",
        options=all_columns,
        default=all_columns[:10] if len(all_columns) > 10 else all_columns,
        key=f"columns_{sheet_name}"
    )

    if not selected_columns:
        selected_columns = all_columns

    # Display the data
    st.dataframe(filtered_df[selected_columns], hide_index=True, use_container_width=True)

    # Download options for this sheet
    st.subheader("Download Sheet Data")

    col1, col2 = st.columns(2)
    with col1:
        # CSV Download
        csv = create_download_csv(filtered_df, st.session_state.file_name, sheet_name)
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name=f"{st.session_state.file_name}_{sheet_name}.csv",
            mime='text/csv',
            key=f"download_csv_{sheet_name}"
        )

    with col2:
        # Excel Download for this sheet
        buffer = create_download_sheet_excel(filtered_df, st.session_state.file_name, sheet_name)
        st.download_button(
            label="Download as Excel",
            data=buffer,
            file_name=f"{st.session_state.file_name}_{sheet_name}.xlsx",
            mime='application/vnd.ms-excel',
            key=f"download_excel_{sheet_name}"
        )

    # Data summary stats
    if st.checkbox("Show summary statistics", key=f"stats_checkbox_{sheet_name}"):
        st.subheader("Summary Statistics")
        stats_df = get_numeric_stats(filtered_df, selected_columns)
        if stats_df is not None:
            st.write(stats_df)
        else:
            st.write("No numeric columns available for statistics.")

def render_data_view():
    """Render the main data view component"""
    try:
        # Get current folder and file names for display
        drive_service, _ = get_google_services()
        folder = get_file_details(drive_service, st.session_state.selected_folder)

        # Display navigation breadcrumbs
        st.markdown(f"📁 **{folder['name']}** / 📊 **{st.session_state.file_name}**")

        # Create tabs for each sheet
        sheet_tabs = st.tabs(st.session_state.sheet_names)

        # Display data for each sheet in its respective tab
        for i, sheet_name in enumerate(st.session_state.sheet_names):
            with sheet_tabs[i]:
                df = st.session_state.sheets_data[sheet_name]
                render_data_sheet(sheet_name, df)

    except Exception as e:
        st.error(f"Error displaying spreadsheet data: {str(e)}")