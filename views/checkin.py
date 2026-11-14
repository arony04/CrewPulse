import streamlit as st

from backend import engine, storage
from backend.indicators import INDICATORS

env, day = st.session_state.env, st.session_state.day
df = storage.history(env, day)
cur = df.iloc[-1]

st.title("Daily check-in")
st.caption(f"Logging for mission day {day}. Your readings replace the simulated ones for this day.")

# ---- 1. form ----
st.header("1. Enter today's readings")
with st.form("checkin"):
    values, cols = {}, st.columns(2)
    typed = [k for k, i in INDICATORS.items() if i["input"] is not None]
    for i, key in enumerate(typed):
        info = INDICATORS[key]
        lo, hi, step = info["input"]
        label = f"{info['name']} ({info['unit']})"
        with cols[i % 2]:
            if info["dec"] == 0:
                values[key] = st.number_input(label, int(lo), int(hi), int(round(float(cur[key]))), int(step),
                                              help=info["how"])
            else:
                values[key] = st.number_input(label, float(lo), float(hi), float(cur[key]), float(step),
                                              format="%.1f", help=info["how"])
    submitted = st.form_submit_button("Save check-in", type="primary")

if submitted:
    values["radiation"] = float(cur["radiation"])       # computed from the mission, not typed
    storage.save_checkin(env, day, values)
    df = storage.history(env, day)

    # ---- 2. results ----
    st.header("2. Check-in results")
    table = engine.results_table(df)[["Indicator", "Latest", "Status", "Normal range", "Drift (SD)"]]
    st.dataframe(table, use_container_width=True, hide_index=True)
    alerts = engine.alerts(df, env)
    if alerts:
        st.warning(alerts[0]["title"] + ": " + alerts[0]["action"])
    else:
        st.success("Everything is in range. Nice work.")

    # ---- 3. rewards ----
    st.header("3. Rewards")
    c = st.columns(3)
    c[0].metric("Streak", f"{storage.streak(env, day)} days")
    c[1].metric("XP", storage.xp(env))
    c[2].metric("Level", storage.xp(env) // 100 + 1)
    for b in storage.badges(env, day, df):
        st.write(f"🏅 {b}")

st.divider()
if st.button("Delete all my check-ins"):
    storage.clear()
    st.rerun()
