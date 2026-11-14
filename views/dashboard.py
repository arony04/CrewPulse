import streamlit as st

from backend import engine, storage, ui
from backend.environments import ENVS
from backend.indicators import HAZARDS, HAZARD_ACTIONS

env, day = st.session_state.env, st.session_state.day
e = ENVS[env]
df = storage.history(env, day)
cur = df.iloc[-1]

st.title("Mission Control")
st.caption(f"{e['label']} · mission day {day}")

# ---- 1. readiness ----
st.header("1. Crew readiness")
c = st.columns(5)
c[0].metric("Readiness", f"{engine.readiness(df)} / 100")
c[1].metric("Radiation used", f"{cur['radiation']:.0f}% of limit")
c[2].metric("Ground reply delay", f"{e['delay_min']:g} min one way")
c[3].metric("Check-in streak", f"{storage.streak(env, day)} days")
total_xp = storage.xp(env)
c[4].metric("Level", total_xp // 100 + 1)
c[4].caption(f"{total_xp} XP")

# ---- 2. hazards ----
st.header("2. Hazard status")
hs = engine.hazard_status(df, env)
for col, (key, info) in zip(st.columns(len(HAZARDS)), HAZARDS.items()):
    with col, st.container(border=True):
        st.markdown(f"**{info['name']}**")
        st.markdown(ui.badge(hs[key]), unsafe_allow_html=True)
        st.caption(info["summary"])

# ---- 3. alerts ----
st.header("3. Alerts")
alerts = engine.alerts(df, env)
if not alerts:
    st.success("No alerts. Every reading is in range and close to your own baseline.")
for a in alerts:
    box = st.error if a["severity"] == 2 else st.warning if a["severity"] == 1 else st.info
    box(f"**{a['title']}**: {a['detail']}\n\n{a['action']}")

# ---- 4. patterns ----
st.header("4. Patterns across indicators")
patterns = engine.patterns(df)
if not patterns:
    st.write("No combined warning patterns right now.")
for p in patterns:
    st.warning(f"**{p['name']}**: {p['detail']}")

# ---- 5. next step ----
st.header("5. Recommended next step")
if alerts:
    top = alerts[0]
    st.markdown(f"**Most urgent: {top['title']}**")
    st.write(top["action"])
    st.markdown("**Steps that help:**")
    for tip in HAZARD_ACTIONS[top["hazard"]]:
        st.write(f"- {tip}")
else:
    st.write("All clear. Log today's check-in to keep your streak going.")