# Universal AI Business Intelligence Assistant

This version adapts its dashboard, analytics, charts, AI Q&A, executive report and baseline forecasting to the columns in one uploaded CSV or Excel file. It does not require a fixed `Sales`, `Profit`, `Product` or `Region` schema.

## Project structure

```text
universal_ai_bi_project/
├── app.py
├── pages/
│   ├── 1_Dashboard.py
│   ├── 2_Analytics.py
│   ├── 3_AI_Assistant.py
│   └── 4_Forecasting.py
├── utils/
│   ├── profiling.py
│   ├── load_data.py
│   ├── eda.py
│   ├── insights.py
│   ├── qa_engine.py
│   ├── ai_engine.py
│   ├── ai_analyst.py
│   ├── report_generator.py
│   └── styles.py
├── charts/
│   ├── chart_engine.py
│   ├── bar_chart.py
│   └── forecast_chart.py
├── models/
│   └── forecasting.py
└── requirements.txt
```

## Run locally

Use your existing Python environment. From this folder:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Gemini is optional for deterministic analytics and local Q&A. To enable Gemini, create `.streamlit/secrets.toml` with:

```toml
GEMINI_API_KEY = "your-real-api-key"
```

Do not commit `secrets.toml` or share your API key.

## How universal behavior works

- Column names are inspected instead of assuming fixed names.
- Numeric columns are classified into likely measures and possible identifiers.
- Date-like columns are detected from their values and names.
- Categorical dimensions are used for group-by charts when suitable.
- KPI cards display only available numeric measures. The app does not invent profit or revenue when those fields are absent.
- Forecasting requires a usable numerical measure and at least five valid observations. A date/time column is optional; without one, observation order is used.
- The forecast is a simple linear-trend baseline. It is not a trained production forecasting model and should be validated on holdout data before business decisions.
- Classification predictions such as churn/attrition are not automatically trained by this version. Those require a clearly identified target column and a separate model-training/evaluation workflow.

## Important integration note

This is a clean replacement project layout based on the Python files supplied for review. Back up your existing project before copying these folders. If your original app uses a different deployment entry point or page layout, merge the files into the matching folders rather than deleting unrelated project files.


AI-powered business analytics platform built using Streamlit, Gemini AI, Pandas, Plotly, and Scikit-Learn.

## Features

- Automated EDA
- Business KPI Dashboard
- AI Data Analyst
- Executive Report Generation
- Sales Forecasting
- Interactive Visualizations

## Technologies

- Python
- Streamlit
- Gemini AI
- Pandas
- Plotly
- Scikit-Learn

## Screenshots
<img width="1470" height="956" alt="Screenshot 2026-06-10 at 3 23 41 AM" src="https://github.com/user-attachments/assets/947f70d3-18ec-41c7-bbba-23725554b02e" />

<img width="1470" height="956" alt="Screenshot 2026-06-10 at 3 24 09 AM" src="https://github.com/user-attachments/assets/68924f62-61e5-406c-b2e6-28df3326f81c" />

<img width="1470" height="956" alt="Screenshot 2026-06-10 at 3 24 37 AM" src="https://github.com/user-attachments/assets/fef9e8ff-861b-4353-84de-6b1685e24012" />

<img width="1470" height="956" alt="Screenshot 2026-06-10 at 3 25 05 AM" src="https://github.com/user-attachments/assets/e2da43d9-ed9b-4090-8f57-9a9dcfd273ab" />

<img width="1470" height="956" alt="Screenshot 2026-06-10 at 3 27 25 AM" src="https://github.com/user-attachments/assets/69bcf547-d9b7-44c4-844d-66041f40610b" />
<img width="1470" height="956" alt="Screenshot 2026-06-10 at 3 27 18 AM" src="https://github.com/user-attachments/assets/95ded6b9-c919-467c-8de3-3545c83c5251" />
<img width="1470" height="956" alt="Screenshot 2026-06-10 at 3 27 07 AM" src="https://github.com/user-attachments/assets/12612b84-ef35-4437-b8fe-93197ca7c440" />




## Installation

pip install -r requirements.txt

streamlit run app.py
