import pandas as pd
import streamlit as st

from backend.indicators import HAZARDS, INDICATORS
from backend.sources import ACCESSED, SOURCES

st.title("Guide and sources")
st.caption("Where every number in this app comes from. Ranges are general adult reference values. "
           "In space, your own baseline matters more than any textbook range.")

# ---- 1. indicators ----
st.header("1. Indicators, ranges and where they come from")
rows = [{
    "Indicator": i["name"], "Hazard": HAZARDS[i["hazard"]]["name"], "Unit": i["unit"],
    "Normal": f"{i['normal'][0]} to {i['normal'][1]}", "Watch": f"{i['watch'][0]} to {i['watch'][1]}",
    "Type": i["kind"], "Basis": i["basis"],
} for i in INDICATORS.values()]
st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

# ---- 2. how to measure ----
st.header("2. How to measure and why it matters")
for info in INDICATORS.values():
    with st.expander(info["name"]):
        st.write(f"**Why:** {info['why']}")
        st.write(f"**How:** {info['how']}")

# ---- 3. sources ----
st.header("3. Sources")
st.caption(f"Primary = agency or guideline body. Secondary = news or explainer, confirm before final use. Checked {ACCESSED}.")
src = pd.DataFrame([{"Publisher": s["publisher"], "Title": s["title"], "Tier": s["tier"],
                     "Used for": s["used_for"], "Link": s["url"]} for s in SOURCES.values()])
st.dataframe(src, use_container_width=True, hide_index=True,
             column_config={"Link": st.column_config.LinkColumn("Link", display_text="open")})

# ---- 4. limits ----
st.header("4. Limits of this tool")
st.write("- Educational prototype, not a medical device and not medical advice.\n"
         "- The mission data is simulated. Mood, social contact, food eaten and the watch margins are app design.\n"
         "- Radiation and exercise figures for the Moon and Mars simulations are assumptions to be replaced with sourced values.")
