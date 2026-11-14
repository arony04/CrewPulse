"""backend/engine.py: turns readings into meaning: status, drift from your baseline, trends, alerts, patterns."""
import numpy as np
import pandas as pd

from .environments import ENVS, AUTONOMY_THRESHOLD_MIN
from .indicators import INDICATORS, HAZARDS, REGIONS, get_status

LABELS = ["Normal", "Watch", "Act now"]
SKIP_DRIFT = {"radiation"}      # cumulative, so it always rises


def status_of(key, value):
    return get_status(key, float(value))


def statuses(df):
    cur = df.iloc[-1]
    return {k: status_of(k, cur[k]) for k in INDICATORS}


# ---------- your own baseline: the first 14 days ----------
def _sd_floor(key):
    lo, hi = INDICATORS[key]["watch"]
    return max(0.03 * (hi - lo), 0.05)


def baseline(df, key):
    first = df[key].head(14)
    return float(first.mean()), max(float(first.std(ddof=0)), _sd_floor(key))


def drift(df, key):
    """How many standard deviations today is from your own baseline."""
    if key in SKIP_DRIFT or len(df) <= 14:
        return 0.0
    mean, sd = baseline(df, key)
    return (float(df[key].iloc[-1]) - mean) / sd


def weekly_trend(df, key, window=14):
    y = df[key].tail(window).to_numpy(float)
    if len(y) < 4:
        return 0.0
    return float(np.polyfit(np.arange(len(y)), y, 1)[0] * 7)


# ---------- what to do: depends on how far the ground is ----------
def triage(severity, delay_min):
    if severity >= 2:
        if delay_min >= AUTONOMY_THRESHOLD_MIN:
            return (f"Autonomous mode: remeasure, follow your treatment protocol, send a full report now, "
                    f"then keep working the problem. A reply takes about {delay_min:g} minutes each way, so do not wait for it.")
        return "Remeasure, then call the flight surgeon now."
    if severity >= 1:
        return "Try the steps below, remeasure tomorrow, and tell the flight surgeon at your next scheduled contact."
    return "Still in range but moving away from your own normal. Keep an eye on it."


def alerts(df, env):
    delay, cur, out = ENVS[env]["delay_min"], df.iloc[-1], []
    for key, info in INDICATORS.items():
        v, s, z = float(cur[key]), status_of(key, cur[key]), drift(df, key)
        if s == 2:
            sev, title, detail = 2, f"{info['name']}: act now", f"{v:g} {info['unit']} is well outside the normal range."
        elif s == 1:
            sev, title, detail = 1, f"{info['name']}: watch", f"{v:g} {info['unit']} is outside the normal range."
        elif abs(z) >= 2.5:
            sev, title = 0.5, f"{info['name']}: drifting"
            detail = f"{v:g} {info['unit']} is normal but {abs(z):.1f} SD {'above' if z > 0 else 'below'} your own baseline."
        else:
            continue
        out.append({"key": key, "hazard": info["hazard"], "severity": sev, "title": title,
                    "detail": detail, "action": triage(sev, delay)})
    return sorted(out, key=lambda a: -a["severity"])


def patterns(df):
    """Combinations of signals that mean more together than apart."""
    s, out = statuses(df), []
    if s["mood"] >= 1 and s["sleep"] >= 1 and (s["social"] >= 1 or weekly_trend(df, "hr") > 0):
        out.append({"name": "Isolation stress pattern",
                    "detail": "Low mood and poor sleep together with less social contact or a rising heart rate. "
                              "Talk to a crewmate and protect your sleep window."})
    if s["temp"] >= 1 and (drift(df, "hr") >= 2 or s["sleep"] >= 1 or s["food"] >= 1):
        out.append({"name": "Possible infection pattern",
                    "detail": "Raised temperature with a faster heart rate, worse sleep or less eating. "
                              "Isolate from crew if you can and log symptoms."})
    if s["exercise"] >= 1 and (drift(df, "sys") >= 1.5 or drift(df, "hr") >= 1.5):
        out.append({"name": "Deconditioning risk",
                    "detail": "Less exercise while heart rate or blood pressure drifts up. Restart daily resistive sessions."})
    if s["radiation"] >= 1:
        out.append({"name": "Radiation budget",
                    "detail": "A large share of your career dose limit is used. Review shielding habits with the flight surgeon."})
    return out


# ---------- roll-ups ----------
def hazard_status(df, env):
    """Status per hazard. Distance has no sensor: its risk is how urgent the worst problem is
    multiplied by how slow the ground is to reply (app design)."""
    st = statuses(df)
    out = {h: max((st[k] for k, i in INDICATORS.items() if i["hazard"] == h), default=0) for h in HAZARDS}
    worst = max(st.values())
    slow = ENVS[env]["delay_min"] >= AUTONOMY_THRESHOLD_MIN
    out["distance"] = worst if slow else (1 if worst == 2 else 0)
    return out


def region_status(df):
    st = statuses(df)
    return {r: max(st[k] for k in info["indicators"]) for r, info in REGIONS.items()}


def readiness(df):
    score = 100
    for s in statuses(df).values():
        score -= 14 if s == 2 else 5 if s == 1 else 0
    return max(0, score)


def results_table(df):
    """One row per indicator: the mission summary."""
    rows, last14 = [], df.tail(14)
    for key, info in INDICATORS.items():
        mean, _ = baseline(df, key)
        rows.append({
            "Indicator": info["name"], "Hazard": HAZARDS[info["hazard"]]["name"], "Unit": info["unit"],
            "Latest": float(df[key].iloc[-1]),
            "Status": LABELS[status_of(key, df[key].iloc[-1])],
            "Normal range": f"{info['normal'][0]} to {info['normal'][1]}",
            "Your baseline": round(mean, 1),
            "Drift (SD)": round(drift(df, key), 1),
            "Trend per week": round(weekly_trend(df, key), 2),
            "Days outside normal (last 14)": int(sum(status_of(key, v) > 0 for v in last14[key])),
        })
    return pd.DataFrame(rows)