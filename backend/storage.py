"""backend/storage.py: saves your check-ins to data/checkins.csv and merges them over the simulated mission."""
from pathlib import Path

import pandas as pd

from .indicators import INDICATORS, get_status
from .simulator import simulate

PATH = Path(__file__).resolve().parent.parent / "data" / "checkins.csv"
COLS = ["env", "day"] + list(INDICATORS)


def load():
    if PATH.exists():
        try:
            return pd.read_csv(PATH)
        except Exception:
            pass
    return pd.DataFrame(columns=COLS)


def save_checkin(env, day, values):
    df = load()
    df = df[~((df["env"] == env) & (df["day"] == day))]
    row = {"env": env, "day": day, **values}
    PATH.parent.mkdir(exist_ok=True)
    pd.concat([df, pd.DataFrame([row])], ignore_index=True)[COLS].to_csv(PATH, index=False)


def clear():
    if PATH.exists():
        PATH.unlink()


def history(env, day):
    """Simulated days up to `day`, with your own check-ins replacing the simulated values."""
    df = simulate(env)
    df = df[df["day"] <= day].copy()
    df[list(INDICATORS)] = df[list(INDICATORS)].astype(float)   # one number type, so check-ins always fit
    logs = load()
    logs = logs[(logs["env"] == env) & (logs["day"] <= day)]
    for _, row in logs.iterrows():
        df.loc[df["day"] == row["day"], list(INDICATORS)] = [row[k] for k in INDICATORS]
    return df.reset_index(drop=True)


def logged_days(env):
    logs = load()
    return set(int(d) for d in logs[logs["env"] == env]["day"])


def streak(env, day):
    days, n = logged_days(env), 0
    while day - n >= 1 and (day - n) in days:
        n += 1
    return n


def xp(env):
    logs, total = load(), 0
    for _, row in logs[logs["env"] == env].iterrows():
        total += 10 + 5 * sum(get_status(k, float(row[k])) == 0 for k in INDICATORS)
    return total


def badges(env, day, df):
    earned, n = [], streak(env, day)
    if logged_days(env):
        earned.append("First check-in")
    if n >= 3:
        earned.append("3-day streak")
    if n >= 7:
        earned.append("7-day streak")
    if all(get_status(k, float(df.iloc[-1][k])) == 0 for k in INDICATORS):
        earned.append("Green sweep (everything normal)")
    return earned
