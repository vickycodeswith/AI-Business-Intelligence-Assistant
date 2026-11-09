"""Lazy Gemini client. The rest of the application works without an API key."""
from __future__ import annotations


import os
import streamlit as st
from google import genai


def get_api_key():
    """Load Gemini API key from environment or Streamlit secrets."""

    api_key = os.getenv("GEMINI_API_KEY")

    if api_key:
        return api_key

    try:
        return st.secrets.get("GEMINI_API_KEY")
    except Exception:
        return None


def ask_gemini(prompt):
    """Send a prompt to Gemini securely."""

    api_key = get_api_key()

    if not api_key:
        return (
            "Gemini API key is missing. "
            "Configure GEMINI_API_KEY in .streamlit/secrets.toml."
        )

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text or "Gemini returned an empty response."

    except Exception as e:
        return f"Gemini API error: {type(e).__name__}: {e}"
