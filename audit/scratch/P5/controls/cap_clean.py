"""P5 clean control: read-only file access and escaped markdown (never executed; parsed only)."""
from pathlib import Path

import streamlit as st


def safe(user: str) -> str:
    with open("data.txt") as fh:
        text = fh.read()
    st.markdown(f"**{user}**")
    return text + Path("x.yaml").read_text()
