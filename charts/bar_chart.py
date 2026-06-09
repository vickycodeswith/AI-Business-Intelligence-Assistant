import plotly.express as px


def sales_by_product_chart(df):

    if "Product" not in df.columns:
        return None

    if "Sales" not in df.columns:
        return None

    sales_data = (
        df.groupby("Product")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        sales_data,
        x="Product",
        y="Sales",
        title="Sales by Product"
    )

    return fig


# Region Chart showing 

def sales_by_region_chart(df):

    if "Region" not in df.columns:
        return None

    if "Sales" not in df.columns:
        return None

    region_data = (
        df.groupby("Region")["Sales"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        region_data,
        x="Region",
        y="Sales",
        title="Sales by Region"
    )

    return fig

def profit_by_product_chart(df):

    if "Product" not in df.columns:
        return None

    if "Profit" not in df.columns:
        return None

    profit_data = (
        df.groupby("Product")["Profit"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        profit_data,
        x="Product",
        y="Profit",
        title="Profit by Product"
    )

    return fig

