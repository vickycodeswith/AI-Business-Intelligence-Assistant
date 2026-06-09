import plotly.express as px


def generate_chart(question, df):

    question = question.lower()

    # Sales by Region

    if (
        "sales" in question
        and
        "region" in question
    ):

        if (
            "Region" in df.columns
            and
            "Sales" in df.columns
        ):

            result = (
                df.groupby("Region")["Sales"]
                .sum()
                .reset_index()
            )

            fig = px.bar(
                result,
                x="Region",
                y="Sales",
                title="Sales By Region"
            )

            return fig

    # Profit by Product

    elif (
        "profit" in question
        and
        "product" in question
    ):

        if (
            "Product" in df.columns
            and
            "Profit" in df.columns
        ):

            result = (
                df.groupby("Product")["Profit"]
                .sum()
                .reset_index()
            )

            fig = px.bar(
                result,
                x="Product",
                y="Profit",
                title="Profit By Product"
            )

            return fig

    return None