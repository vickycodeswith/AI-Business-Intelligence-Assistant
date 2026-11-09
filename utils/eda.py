import pandas as pd
from utils.profiling import profile_dataset


def dataset_info(df):
    profile = profile_dataset(df)
    return {key: profile[key] for key in ("rows", "columns", "missing_values", "duplicate_rows")}


def column_information(df):
    return profile_dataset(df)["column_details"]


def column_categories(df):
    profile = profile_dataset(df)
    return profile["measure_columns"], profile["dimension_columns"]


def statistical_summary(df):
    numeric = df.select_dtypes(include="number")
    if numeric.empty:
        return pd.DataFrame({"Message": ["No numerical columns are available for statistical summary."]})
    return numeric.describe().T
