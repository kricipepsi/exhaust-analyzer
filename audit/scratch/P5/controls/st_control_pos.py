"""P5 planted positive control: user text reaches unsafe HTML; a subprocess and a file write run."""
import subprocess
import tempfile

import streamlit as st

t = st.text_input("t", key="t")
if st.button("go"):
    subprocess.run(["true"], check=False)
    with tempfile.NamedTemporaryFile("w", delete=True) as fh:
        fh.write("x")
    st.markdown(f"<div>{t}</div>", unsafe_allow_html=True)
