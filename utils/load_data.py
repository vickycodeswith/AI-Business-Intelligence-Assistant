import pandas as pd


def load_file(uploaded_file):

    if uploaded_file.name.endswith(".csv"):

        encodings = [
            "utf-8",
            "utf-8-sig",
            "latin1",
            "cp1252"
        ]

        separators = [
            ",",
            ";",
            "\t",
            "|"
        ]

        for encoding in encodings:

            for sep in separators:

                try:

                    uploaded_file.seek(0)

                    df = pd.read_csv(
                        uploaded_file,
                        encoding=encoding,
                        sep=sep
                    )

                    if len(df.columns) > 1:
                        return df

                except Exception:
                    continue

        raise ValueError(
            "Unable to read CSV file. Unsupported format."
        )

    elif uploaded_file.name.endswith(".xlsx"):

        return pd.read_excel(uploaded_file)

    else:

        raise ValueError(
            "Unsupported file format."
        )