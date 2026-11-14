"""backend/ui.py: small shared display helpers."""
from .engine import LABELS

COLORS = {0: "#5fd394", 1: "#f0b04a", 2: "#ff8a80"}
BACKGROUNDS = {0: "rgba(46,158,106,.20)", 1: "rgba(224,160,48,.20)", 2: "rgba(208,69,59,.24)"}


def badge(status):
    """HTML pill: use with st.markdown(..., unsafe_allow_html=True). Label always shown, never colour alone."""
    return (f'<span style="background:{BACKGROUNDS[status]};color:{COLORS[status]};padding:2px 12px;'
            f'border-radius:999px;font-weight:600;font-size:.82rem">{LABELS[status]}</span>')
