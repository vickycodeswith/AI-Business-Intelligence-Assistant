"""Backward-compatible wrappers around dynamic chart generation."""
from utils.chart_engine import generate_chart


def sales_by_product_chart(df):
    return generate_chart("show the main metric by product", df)


def sales_by_region_chart(df):
    return generate_chart("show the main metric by region", df)


def profit_by_product_chart(df):
    return generate_chart("show the main metric by product", df)
