"""P5 clean control: the same page, but user text is escaped and no subprocess or write runs."""
import html

import streamlit as st

t = st.text_input("t", key="t")
if st.button("go"):
    st.markdown(f"<div>{html.escape(t)}</div>", unsafe_allow_html=True)
