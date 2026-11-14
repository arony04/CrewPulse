"""backend/simulator.py: a repeatable 180-day mission so the app has history to analyse.

The mission is SIMULATED. It shows the app's logic: slow drift from hazards plus one infection event.
Same environment gives the same mission every time (seeded random numbers).
"""
import math
import random
from functools import lru_cache

import pandas as pd

from .environments import ENVS, MISSION_DAYS, CAREER_LIMIT_MSV
from .indicators import INDICATORS


def _clamp(x, lo, hi):
    return max(lo, min(hi, x))


@lru_cache(maxsize=None)
def _simulate(env):
    e = ENVS[env]
    rng = random.Random(f"crewpulse-{env}")
    micro = 1.0 - e["gravity_g"]          # 1.0 = microgravity, about 0.83 on the Moon
    dose, rows = 0.0, []
    for d in range(1, MISSION_DAYS + 1):
        t = d / MISSION_DAYS
        slump = math.sin(math.pi * t) * e["iso"]            # morale dips mid-mission
        fever = {112: 0.5, 113: 1.0, 114: 1.0, 115: 0.7, 116: 0.4}.get(d, 0.0)   # infection, peaks days 113-114
        dose += e["rad_msv_day"] * (1 + rng.gauss(0, 0.05))
        v = {
            "radiation": dose / CAREER_LIMIT_MSV * 100,
            "mood": _clamp(4.5 - 1.6 * slump - 0.7 * fever + rng.gauss(0, 0.4), 1, 5),
            "sleep": _clamp(7.6 - 1.5 * e["iso"] * t - 0.3 * slump - 1.5 * fever + rng.gauss(0, 0.35), 0, 14),
            "social": _clamp(3.5 - 2.0 * e["iso"] * t + rng.gauss(0, 0.4), 0, 24),
            "hr": 66 + 9 * micro * t + 22 * fever + rng.gauss(0, 2.5),
            "sys": 112 + 8 * micro * t + rng.gauss(0, 3),
            "dia": 72 + 4 * micro * t + rng.gauss(0, 2.5),
            "exercise": _clamp(85 - 40 * t * (0.4 + 0.6 * e["iso"]) + rng.gauss(0, 8), 0, 300),
            "temp": 36.6 + 2.0 * fever + rng.gauss(0, 0.15),
            "glucose": 88 + 14 * t + rng.gauss(0, 4),
            "food": _clamp(100 - 15 * slump - 25 * fever + rng.gauss(0, 4), 0, 150),
        }
        row = {"day": d}
        for k, x in v.items():
            dec = INDICATORS[k]["dec"]
            row[k] = int(round(x)) if dec == 0 else round(x, dec)
        rows.append(row)
    return pd.DataFrame(rows)


def simulate(env):
    return _simulate(env).copy()
