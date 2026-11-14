import streamlit as st

from backend.environments import ENVS, MISSION_DAYS

st.set_page_config(page_title="CrewPulse", page_icon="🧑‍🚀", layout="wide")

st.session_state.setdefault("env", "station")
st.session_state.setdefault("day", 60)

with st.sidebar:
    st.title("🧑‍🚀 CrewPulse")
    st.caption("Self-check health monitor for long-duration missions")
    st.selectbox("Where are you?", list(ENVS), format_func=lambda k: ENVS[k]["label"], key="env")
    st.slider("Mission day", 1, MISSION_DAYS, key="day",
              help="Drag to replay the mission. Days you check in yourself replace the simulated ones.")
    st.info(ENVS[st.session_state.env]["note"])

pages = st.navigation([
    st.Page("views/dashboard.py", title="Mission Control", icon="🛰️"),
    st.Page("views/hazards.py", title="Hazards", icon="⚠️"),
    st.Page("views/trends.py", title="Trends and results", icon="📈"),
    st.Page("views/body_map.py", title="3D body map", icon="🫀"),
    st.Page("views/checkin.py", title="Check-in", icon="📝"),
    st.Page("views/guide.py", title="Guide and sources", icon="📚"),
])
pages.run()
