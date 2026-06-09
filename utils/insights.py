def generate_insights(df):

    insights = {}

    # Sales Insights
    if "Sales" in df.columns:

        insights["total_sales"] = df["Sales"].sum()

        insights["average_sales"] = round(
            df["Sales"].mean(), 2
        )

    # Profit Insights
    if "Profit" in df.columns:

        insights["average_profit"] = round(
            df["Profit"].mean(), 2
        )

        insights["total_profit"] = df["Profit"].sum()

    # Product Insights
    if "Product" in df.columns:

        top_product = (
            df.groupby("Product")["Sales"]
            .sum()
            .idxmax()
        )

        insights["top_product"] = top_product

    if "Region" in df.columns:

        top_region = (
            df.groupby("Region")["Sales"]
            .sum()
            .idxmax()
        )

        insights["top_region"] = top_region

    return insights

# Recommendation System function 

def generate_recommendations(insights):

    recommendations = []

    top_product = insights.get("top_product")

    top_region = insights.get("top_region")

    if top_product:

        recommendations.append(
            f"Increase focus on {top_product} as it is the best-selling product."
        )

    if top_region:

        recommendations.append(
            f"Expand marketing efforts in {top_region} region since it generates the highest revenue."
        )

    return recommendations