import plotly.graph_objects as go
import streamlit as st

from backend import engine, storage
from backend.indicators import INDICATORS
from backend.ui import COLORS

env, day = st.session_state.env, st.session_state.day
df = storage.history(env, day)

st.title("Trends and results")

# ---- 1. chart ----
st.header("1. Trend chart")
left, right = st.columns([2, 1])
key = left.selectbox("Indicator", list(INDICATORS), format_func=lambda k: INDICATORS[k]["name"])
window = right.selectbox("Window", ["Last 14 days", "Last 30 days", "Last 90 days", "Whole mission"], index=1)
n = {"Last 14 days": 14, "Last 30 days": 30, "Last 90 days": 90}.get(window, len(df))
info, data = INDICATORS[key], df.tail(n)
mean, _ = engine.baseline(df, key)

fig = go.Figure()
lo, hi = info["normal"]
fig.add_hrect(y0=lo, y1=hi, fillcolor="#2e9e6a", opacity=0.14, line_width=0, annotation_text="normal range",
              annotation_position="top left")
fig.add_trace(go.Scatter(x=data["day"], y=data[key], mode="lines+markers", name=info["name"],
                         line=dict(color="#6ea2ff", width=2),
                         marker=dict(size=7, color=[COLORS[engine.status_of(key, v)] for v in data[key]])))
if key not in engine.SKIP_DRIFT:
    fig.add_hline(y=mean, line_dash="dash", line_color="#93a4ba", annotation_text="your baseline")
fig.update_layout(height=380, margin=dict(l=10, r=10, t=30, b=10), xaxis_title="Mission day",
                  yaxis_title=info["unit"], showlegend=False)
st.plotly_chart(fig, use_container_width=True)

trend = engine.weekly_trend(df, key)
direction = "steady" if abs(trend) < 0.05 * max(abs(mean), 1) else ("rising" if trend > 0 else "falling")
st.write(f"**{info['name']}** is {direction} ({trend:+.2f} {info['unit']} per week over the last 14 days). "
         f"Dot colour shows status: green normal, amber watch, red act now.")

# ---- 2. mission summary ----
st.header("2. Mission summary")
st.caption("Drift (SD) compares today with your own first 14 days. Over about 2.5 means it is moving away from your normal.")
st.dataframe(engine.results_table(df), use_container_width=True, hide_index=True)

# ---- 3. export ----
st.header("3. Export")
st.download_button("Download full history (CSV)", df.to_csv(index=False), file_name="crewpulse_history.csv",
                   mime="text/csv")
