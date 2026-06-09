def dataset_info(df):

    info = {

        "rows": df.shape[0],

        "columns": df.shape[1],

        "missing_values": df.isnull().sum().sum(),

        "duplicate_rows": df.duplicated().sum()

    }

    return info

def column_information(df):

    column_info = {

        "Column Name": df.columns,

        "Data Type": df.dtypes.astype(str)

    }

    return column_info

def column_categories(df):

    numerical_cols = df.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()

    categorical_cols = df.select_dtypes(
        include=["object"]
    ).columns.tolist()

    return numerical_cols, categorical_cols

def statistical_summary(df):
    summary = df.describe()
    return summary

