from utils.ai_engine import ask_gemini


def analyze_data_with_ai(
    question,
    df
):

    data_sample = df.head(20).to_string()

    prompt = f"""
You are a Senior Data Analyst and Business Consultant.

Analyze the dataset sample below.

Dataset:

{data_sample}

User Question:

{question}

Rules:

1. Answer in business language.
2. Be concise.
3. Use numbers when possible.
4. Give actionable insights.
5. If data is insufficient, mention it.

Answer:
"""

    return ask_gemini(prompt)