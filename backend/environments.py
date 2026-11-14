"""backend/environments.py: where the crew is. Changes radiation, gravity, isolation and the ground-reply delay."""

MISSION_DAYS = 180
CAREER_LIMIT_MSV = 600        # proposed NASA career limit (see sources: nas_radiation)
AUTONOMY_THRESHOLD_MIN = 5    # app design: at or above this delay, the crew must act first and report second

ENVS = {
    "station": {
        "label": "Space station (low Earth orbit)", "delay_min": 0.0, "gravity_g": 0.0, "iso": 0.6,
        "rad_msv_day": 0.82,   # 300 mSv per year / 365 (source: space_radiation)
        "note": "Earth's magnetic field shields you partly and the ground is a call away. Keep to the exercise routine.",
    },
    "moon": {
        "label": "Lunar surface base", "delay_min": 0.02, "gravity_g": 0.17, "iso": 0.8,
        "rad_msv_day": 1.0,    # ASSUMPTION for the simulation: replace with a sourced figure
        "note": "Partial gravity helps bones less than Earth does. Dust and isolation add risk.",
    },
    "mars": {
        "label": "Mars transit (spacecraft)", "delay_min": 20.0, "gravity_g": 0.0, "iso": 1.0,
        "rad_msv_day": 1.8,    # ASSUMPTION for the simulation: replace with a sourced figure
        "note": "Deep space: weakest shielding, longest delay. Ground help is slow, so lean on your baseline and report early.",
    },
}
