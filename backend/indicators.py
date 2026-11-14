"""backend/indicators.py: hazards, indicators and ranges. Every number points to a source in sources.py.

normal = (low, high)  counts as normal
watch  = wider range  counts as watch
outside watch         counts as "act now"
basis tells the truth about each number: guideline, proposal, or app design.
"""

HAZARDS = {
    "radiation": {"name": "Space radiation",
                  "summary": "Energetic particles raise long-term cancer, heart and nervous-system risk."},
    "isolation": {"name": "Isolation and confinement",
                  "summary": "A small crew in a small space with no escape affects sleep, mood and teamwork."},
    "distance": {"name": "Distance from Earth",
                 "summary": "Help is far away and replies are delayed, so you must judge and act on your own health."},
    "gravity": {"name": "Gravity fields",
                "summary": "Changed gravity shifts body fluids and weakens bones, muscles and the heart."},
    "closed": {"name": "Hostile closed environment",
               "summary": "Recycled air, shared surfaces and limited food affect immunity and nutrition."},
}

# General guidance written for this app (app design), not quotations from the sources.
HAZARD_ACTIONS = {
    "radiation": ["Rest and sleep in the best-shielded part of the vehicle when you can.",
                  "Log your dosimeter reading every day so the running total is never a surprise.",
                  "Report a sudden jump in dose to the flight surgeon at your next scheduled contact."],
    "isolation": ["Keep a fixed sleep window and dim the lights in the evening.",
                  "Book a call home or a hobby block every day, and eat with the crew.",
                  "Tell a crewmate how you feel. Saying it out loud helps."],
    "distance": ["Read your protocol while you feel well, not when you need it.",
                 "When the ground is minutes away, act first and report second.",
                 "Send a complete report: readings, trend, what you tried and what happened."],
    "gravity": ["Do the resistive and treadmill sessions every day.",
                "Drink the planned fluids; remeasure blood pressure after 10 minutes of rest.",
                "Report back pain or a new muscle ache to the flight surgeon at your next scheduled contact."],
    "closed": ["Eat the full planned meals and note any you skip.",
               "Wipe shared surfaces and mask up if a crewmate is ill.",
               "Log symptoms such as cough, rash or unusual tiredness."],
}

HAZARD_SOURCES = {
    "radiation": ["nasa_radiation_brief", "nas_radiation"],
    "isolation": ["nasa_hazards", "pmc_red_risks", "cdc_sleep"],
    "distance": ["nasa_hazards", "space_mars_risks", "nasa_mda"],
    "gravity": ["nasa_hazards", "nasa_risks", "aha_bp", "mayo_hr"],
    "closed": ["nasa_hazards", "medlineplus_temp", "cdc_glucose"],
}

# input: (min, max, step) for the check-in form. None = computed by the app, not typed.
INDICATORS = {
    "radiation": {
        "name": "Radiation (share of career limit)", "unit": "% of 600 mSv", "hazard": "radiation", "kind": "computed",
        "normal": (0, 50), "watch": (0, 80), "dec": 0, "input": None,
        "basis": "NASA career limit is 600 mSv, universal for all astronauts (NASA technical brief; National Academies recommended it); the 50% and 80% steps are app design",
        "sources": ["nasa_radiation_brief", "nas_radiation"],
        "how": "Read the personal dosimeter and add the daily dose to your running total.",
        "why": "Dose builds up for the whole mission and cannot be undone. The running total against the career limit is what counts."},
    "mood": {
        "name": "Mood", "unit": "1-5", "hazard": "isolation", "kind": "self-report",
        "normal": (4, 5), "watch": (3, 5), "dec": 0, "input": (1, 5, 1),
        "basis": "app design: self-reported scale (1 very low, 5 very good)", "sources": ["nasa_hazards", "pmc_red_risks"],
        "how": "Rate your mood honestly at the same time every day.",
        "why": "Isolation, confinement and distance from Earth are linked to low mood and conflict. You are the best sensor for this."},
    "sleep": {
        "name": "Sleep", "unit": "hours", "hazard": "isolation", "kind": "measured",
        "normal": (7, 9), "watch": (6, 10), "dec": 1, "input": (0.0, 14.0, 0.1),
        "basis": "CDC: at least 7 h for adults; 7-9 h from Sleep Foundation; the watch margins are app design",
        "sources": ["cdc_sleep", "sleep_foundation"],
        "how": "Use the sleep tracker, or estimate from your sleep log.",
        "why": "Odd light cycles, noise and confinement disrupt sleep. Sleep loss hurts mood, judgement and immunity."},
    "social": {
        "name": "Social contact", "unit": "hours/day", "hazard": "isolation", "kind": "self-report",
        "normal": (2, 24), "watch": (1, 24), "dec": 1, "input": (0.0, 24.0, 0.5),
        "basis": "app design: self-reported hours of real conversation or calls", "sources": ["nasa_hazards"],
        "how": "Count time spent talking with crew or family, not just working alongside them.",
        "why": "Withdrawal from the crew is an early sign of isolation stress."},
    "hr": {
        "name": "Resting heart rate", "unit": "bpm", "hazard": "gravity", "kind": "measured",
        "normal": (60, 100), "watch": (50, 110), "dec": 0, "input": (30, 200, 1),
        "basis": "Mayo Clinic: 60-100 bpm normal for adults; the watch margin is app design", "sources": ["mayo_hr"],
        "how": "Sit still for 5 minutes, then read the wrist or chest sensor.",
        "why": "Fluids shift toward the head in microgravity and the heart adapts. A rising resting rate is an early signal."},
    "sys": {
        "name": "Blood pressure (top)", "unit": "mmHg", "hazard": "gravity", "kind": "measured",
        "normal": (90, 119), "watch": (85, 139), "dec": 0, "input": (60, 220, 1),
        "basis": "AHA: normal under 120, stage 1 from 130, stage 2 from 140; Mayo Clinic: low is below 90; the 85 margin is app design",
        "sources": ["aha_bp", "mayo_low_bp"],
        "how": "Seated, cuff at heart level, arm relaxed; take two readings a minute apart.",
        "why": "Spaceflight changes how blood is distributed and how vessels behave, so pressure is tracked on long missions."},
    "dia": {
        "name": "Blood pressure (bottom)", "unit": "mmHg", "hazard": "gravity", "kind": "measured",
        "normal": (60, 79), "watch": (55, 89), "dec": 0, "input": (40, 140, 1),
        "basis": "AHA: normal under 80, stage 1 from 80, stage 2 from 90; Mayo Clinic: low is below 60; the 55 margin is app design",
        "sources": ["aha_bp", "mayo_low_bp"],
        "how": "Comes from the same reading as the top number.",
        "why": "Read together with the top number. A high bottom number means vessels stay tense between beats."},
    "exercise": {
        "name": "Resistive exercise", "unit": "min/day", "hazard": "gravity", "kind": "self-report",
        "normal": (60, 240), "watch": (30, 240), "dec": 0, "input": (0, 300, 5),
        "basis": "NASA: ISS crew average about 2 hours of exercise a day across resistive, treadmill and cycle; the 60 min target and 30 min watch line are app design", "sources": ["nasa_exercise"],
        "how": "Total minutes on the resistance device and treadmill today.",
        "why": "Without weight on them, bones and muscles weaken within weeks. Daily loading is the main defence."},
    "temp": {
        "name": "Body temperature", "unit": "°C", "hazard": "closed", "kind": "measured",
        "normal": (36.1, 37.2), "watch": (35.5, 38.0), "dec": 1, "input": (34.0, 41.0, 0.1),
        "basis": "MedlinePlus: 36.1-37.2 C normal, fever above 38 C; the low margin is app design", "sources": ["medlineplus_temp"],
        "how": "Forehead or ear thermometer after 10 minutes at rest.",
        "why": "Immune function shifts in spaceflight and a closed cabin spreads germs. A fever may be the first sign."},
    "glucose": {
        "name": "Fasting glucose", "unit": "mg/dL", "hazard": "closed", "kind": "measured",
        "normal": (70, 99), "watch": (60, 125), "dec": 0, "input": (40, 400, 1),
        "basis": "CDC: normal 99 or lower, prediabetes 100-125, diabetes 126 or higher; CDC: low is below 70; the 60 margin is app design",
        "sources": ["cdc_glucose", "cdc_low_glucose"],
        "how": "Before eating, with the finger-prick meter.",
        "why": "Stress, reduced activity and food changes can disturb blood sugar and nutrition."},
    "food": {
        "name": "Food eaten", "unit": "% of plan", "hazard": "closed", "kind": "self-report",
        "normal": (90, 120), "watch": (70, 120), "dec": 0, "input": (0, 150, 5),
        "basis": "app design: share of the planned meals actually eaten", "sources": ["nasa_risks"],
        "how": "Estimate the share of today's planned food you actually ate.",
        "why": "Eating too little is a known risk on long missions and shows up in energy, mood and bone health."},
}

# Body regions for the 3D map: which indicators sit in which area.
REGIONS = {
    "brain": {"title": "Brain and behaviour", "indicators": ["mood", "sleep", "social"], "hazard": "isolation",
              "info": "Controls sleep, mood and decisions. These are often the first things to slip."},
    "heart": {"title": "Heart and circulation", "indicators": ["hr", "sys", "dia"], "hazard": "gravity",
              "info": "Pumps blood against changing gravity. Rate and pressure show how well you adapt."},
    "gut": {"title": "Metabolism and immunity", "indicators": ["temp", "glucose", "food"], "hazard": "closed",
            "info": "Digestion, blood sugar and your defence against infection."},
    "bone": {"title": "Bone and muscle", "indicators": ["exercise"], "hazard": "gravity",
             "info": "Bones lose density and muscles shrink when they carry no weight."},
    "body": {"title": "Whole body (radiation)", "indicators": ["radiation"], "hazard": "radiation",
             "info": "Radiation reaches every tissue. The glowing shell around the body shows your running dose."},
}


def get_status(key, value):
    """Return 0 = normal, 1 = watch, 2 = act now."""
    info = INDICATORS[key]
    low, high = info["normal"]
    if low <= value <= high:
        return 0
    low, high = info["watch"]
    if low <= value <= high:
        return 1
    return 2