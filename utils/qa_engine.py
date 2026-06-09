import pandas as pd
def answer_question(question, df, insights):

    question = question.lower()

    profit_keywords = [
        "total profit",
        "overall profit",
        "company profit",
        "net profit"
    ]

    sales_keywords = [
        "total sales",
        "overall sales",
        "total revenue",
        "company revenue"
    ]

    # TOP PRODUCT

    if (
        any(word in question for word in ["product", "item"])
        and
        any(word in question for word in ["top", "best", "highest", "most", "selling",  "maximum" ])
    ):

        return f"🏆 Top Product: {insights.get('top_product', 'N/A')}"

    # TOP REGION

    elif (
        "region" in question
        and
        any(
            word in question
            for word in [
                "top",
                "best",
                "highest",
                "most",
                "revenue",
                "sales",
                "maximum"
            ]
        )
    ):
        return f"🌍 Top Region: {insights.get('top_region', 'N/A')}"

    # SALES BY REGION

    elif "sales" in question and "region" in question:

        if (
            "Region" not in df.columns
            or
            "Sales" not in df.columns
           ):
            return "Region or Sales column not found."

        result = (
            df.groupby("Region")["Sales"]
            .sum()
            .sort_values(ascending=False)
        )

        return result.to_string()

    # PROFIT BY PRODUCT

    elif (

        ("profit" in question or "profitable" in question)
        and
        "product" in question
        ):

        result = (
            df.groupby("Product")["Profit"]
            .sum()
            .sort_values(ascending=False)
        )

        return result.to_string()

    # TOTAL SALES

    elif any(keyword in question for keyword in sales_keywords):

        return f"💰 Total Sales: {insights.get('total_sales', 0)}"

    # TOTAL PROFIT

    elif any(keyword in question for keyword in profit_keywords):

        return f"📈 Total Profit: {insights.get('total_profit', 0)}"

    return "I don't understand that question yet."


