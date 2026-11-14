import streamlit as st

from backend import engine, storage, ui
from backend.environments import ENVS, AUTONOMY_THRESHOLD_MIN
from backend.indicators import HAZARDS, HAZARD_ACTIONS, HAZARD_SOURCES, INDICATORS
from backend.sources import link

env, day = st.session_state.env, st.session_state.day
df = storage.history(env, day)
cur = df.iloc[-1]
hs = engine.hazard_status(df, env)
e = ENVS[env]

st.title("The five hazards")
st.caption("NASA's Human Research Program groups spaceflight health risks under five hazards. "
           "Each tab shows what the hazard does and which of your readings it affects.")

tabs = st.tabs([h["name"] for h in HAZARDS.values()])
for tab, (hkey, hazard) in zip(tabs, HAZARDS.items()):
    with tab:
        st.subheader(hazard["name"])
        st.markdown(ui.badge(hs[hkey]), unsafe_allow_html=True)
        st.write(hazard["summary"])

        keys = [k for k, i in INDICATORS.items() if i["hazard"] == hkey]
        if keys:
            st.markdown("**Your readings**")
            for k in keys:
                info = INDICATORS[k]
                s = engine.status_of(k, cur[k])
                left, mid, right = st.columns([3, 2, 2])
                left.markdown(f"**{info['name']}**")
                mid.markdown(f"{float(cur[k]):g} {info['unit']}")
                right.markdown(ui.badge(s), unsafe_allow_html=True)
                with st.expander(f"Why it matters and how to measure {info['name'].lower()}"):
                    st.write(info["why"])
                    st.write(f"**How to measure:** {info['how']}")
                    st.caption(f"Normal range: {info['normal'][0]} to {info['normal'][1]} {info['unit']}")
        else:
            st.markdown("**Your situation**")
            st.metric("Ground reply delay", f"{e['delay_min']:g} min each way")
            if e["delay_min"] >= AUTONOMY_THRESHOLD_MIN:
                st.warning(f"Autonomous mode: the ground is at least {AUTONOMY_THRESHOLD_MIN} minutes away. "
                           "For an act-now alert, act first and report second.")
            else:
                st.success("Ground contact is quick. For an act-now alert, call the flight surgeon.")
            st.caption("This hazard has no sensor. Its status combines how urgent your worst alert is with how slow the ground is to reply.")

        st.markdown("**What to do**")
        for tip in HAZARD_ACTIONS[hkey]:
            st.write(f"- {tip}")
        st.markdown("**Sources**")
        for sid in HAZARD_SOURCES[hkey]:
            st.markdown(f"- {link(sid)}")
