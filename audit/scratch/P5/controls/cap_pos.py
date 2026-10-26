"""P5 planted capability sinks (never executed; parsed only)."""
import socket
import subprocess
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


def sinks(user: str) -> None:
    subprocess.run(["ls", user])
    socket.create_connection(("example.org", 80))
    Path("out.txt").write_text(user)
    with open("log.txt", "a") as fh:
        fh.write(user)
    st.markdown(f"<p>{user}</p>", unsafe_allow_html=True)
    components.html(user)
