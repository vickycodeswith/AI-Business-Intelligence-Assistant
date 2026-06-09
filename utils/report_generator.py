from utils.ai_engine import ask_gemini


def generate_executive_report(df):

    data_sample = df.head(50).to_string()

    prompt = f"""
You are a Senior Data Analyst and Business Consultant.

Analyze the dataset below and generate a concise executive report.

Dataset:

{data_sample}

Instructions:

- Use simple business language.
- Keep each section 2-4 lines maximum.
- Focus on important findings only.
- Use bullet points.
- Mention actual numbers when available.

Format:

## Executive Summary

## Key Trends

## Top Products

## Top Regions

## Risks

## Growth Opportunities

## Recommendations
"""

    report = ask_gemini(prompt)

    return report