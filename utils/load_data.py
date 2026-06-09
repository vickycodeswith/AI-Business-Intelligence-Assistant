import pandas as pd


def load_file(uploaded_file):
    
    if uploaded_file is None:
        return None

    file_name = uploaded_file.name

    if file_name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)

    elif file_name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)

    else:
        return None

    return df
