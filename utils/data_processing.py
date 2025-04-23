import pandas as pd
from services.google_service import get_sheet_data


def values_to_dataframe(values):
    """Convert sheet values to DataFrame"""
    if not values:
        return pd.DataFrame()

    # Convert to DataFrame
    df = pd.DataFrame(values)
    # Set first row as header
    df.columns = df.iloc[0]

    # Handle empty or duplicate column names
    if None in df.columns or df.columns.duplicated().any():
        # Replace None with named columns
        new_cols = []
        for i, col in enumerate(df.columns):
            if col is None or col in new_cols:
                new_cols.append(f'Column_{i + 1}')
            else:
                new_cols.append(col)
        df.columns = new_cols

    df = df.iloc[1:].reset_index(drop=True)
    return df


def get_all_sheets_data(sheets_service, spreadsheet_id, sheet_names):
    """Read all sheets from a Google Spreadsheet"""
    print(f'Getting data from {sheet_names}')
    sheets_data = {}
    for sheet_name in sheet_names:
        values = get_sheet_data(sheets_service, spreadsheet_id, sheet_name)
        df = values_to_dataframe(values)
        sheets_data[sheet_name] = df

    return sheets_data


def apply_filters(df, filter_settings):
    """Apply filters to a dataframe"""
    filtered_df = df.copy()
    for col, values in filter_settings.items():
        if isinstance(values, list):
            filtered_df = filtered_df[filtered_df[col].isin(values)]
        else:
            # Text filter - case insensitive contains
            filtered_df = filtered_df[
                filtered_df[col].astype(str).str.contains(values, case=False, na=False)]
    return filtered_df


def apply_search(df, search_term):
    """Apply search across all columns in a dataframe"""
    if not search_term:
        return df

    # Search across all columns
    mask = pd.Series(False, index=df.index)
    for col in df.columns:
        mask = mask | df[col].astype(str).str.contains(search_term, case=False, na=False)
    return df[mask]


def get_numeric_stats(df, columns):
    """Get numeric statistics for selected columns"""
    numeric_df = df.copy()
    for col in columns:
        try:
            numeric_df[col] = pd.to_numeric(numeric_df[col])
        except:
            pass

    # Get numeric columns
    numeric_cols = numeric_df.select_dtypes(include=['number']).columns

    if len(numeric_cols) > 0:
        return numeric_df[numeric_cols].describe()
    return None