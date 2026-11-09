from __future__ import annotations

import pandas as pd
from utils.ai_engine import ask_gemini
from utils.profiling import profile_dataset
from utils.insights import generate_insights


def generate_executive_report(df: pd.DataFrame) -> str:
    profile = profile_dataset(df)
    insights = generate_insights(df)
    lines = [
        "# Executive Data Report",
        "",
        "## Dataset overview",
        f"- Records: {profile['rows']:,}",
        f"- Columns: {profile['columns']:,}",
        f"- Missing cells: {profile['missing_values']:,}",
        f"- Duplicate rows: {profile['duplicate_rows']:,}",
        "",
        "## Numerical measures",
    ]
    if insights["metrics"]:
        for col, values in insights["metrics"].items():
            lines.append(f"- **{col}:** total {values['sum']:,.2f}; average {values['mean']:,.2f}; minimum {values['min']:,.2f}; maximum {values['max']:,.2f} (n={values['count']:,}).")
    else:
        lines.append("- No numeric measures were detected; quantitative metrics cannot be calculated.")

    lines.extend(["", "## Highest-value categories"])
    if insights["breakdowns"]:
        for dimension, result in insights["breakdowns"].items():
            lines.append(f"- **{dimension}:** {result['top_category']} has the largest summed {result['metric']} ({result['top_value']:,.2f}).")
    else:
        lines.append("- No suitable categorical breakdowns were detected.")

    lines.extend(["", "## Data quality notes"])
    lines.append(f"- {profile['missing_values']:,} missing cells and {profile['duplicate_rows']:,} duplicate rows were detected.")
    lines.append("- Forecasts and predictions should be treated as estimates and validated against held-out data before business use.")

    # Use Gemini to add narrative only when configured; retain deterministic report otherwise.
    narrative_prompt = (
        "Based only on these calculated facts, write 3 concise business observations and 2 practical next steps. "
        "Do not add unsupported claims or repeat invented metrics.\n\n" + "\n".join(lines)
    )
    narrative = ask_gemini(narrative_prompt)
    if narrative and not narrative.startswith("Gemini is not configured") and not narrative.startswith("Gemini could not"):
        lines.extend(["", "## AI commentary", narrative])
    return "\n".join(lines)
