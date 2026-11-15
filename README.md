# CrewPulse

Self-check health monitor for astronauts on long-duration missions (NASA Space Apps 2026). Built around NASA's five spaceflight hazards.

## Run it
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```
Use the sidebar to pick where you are (station, lunar base, Mars transit) and drag the mission day slider.

## Structure
```
app.py                  navigation and sidebar controls
RESEARCH.md             sources, trust ladder, open questions
backend/
  sources.py            every source with link and tier
  indicators.py         hazards, indicators, ranges, explanations
  environments.py       station, Moon, Mars: radiation, gravity, delay
  simulator.py          repeatable 180-day mission
  engine.py             status, baseline drift, trends, alerts, patterns
  storage.py            check-ins saved to data/checkins.csv, streak, XP
  ui.py                 status badges
views/
  dashboard.py          Mission Control: readiness, hazards, alerts, patterns, next step
  hazards.py            one tab per hazard
  trends.py             chart, mission summary table, CSV export
  body_map.py           3D body with beating heart
  checkin.py            form, results, rewards
  guide.py              ranges, how to measure, sources, limits
```

## Demo script
1. Mars transit, day 20: everything green.
2. Drag to day 114: infection pattern, drift alerts, autonomous-mode advice because the ground is 20 minutes away.
3. Switch to station: same alert, but advice says call the flight surgeon.
4. Open the 3D body map and the Trends page. Log a check-in and show streak and XP.
5. Show the Guide page: every number has a source or is labelled app design.

Educational prototype, not a medical device.


## Current limits and next step

CrewPulse is a prototype. Today it uses simulated mission data and manual check-ins: the person types in their readings on the Check-in page. It is not connected to any real sensors.

In a real mission, the same app would take its readings from crew health devices, such as a wearable for heart rate and temperature, a blood pressure cuff, a glucose meter, a radiation dosimeter and a sleep tracker. The analysis stays the same: status, drift from the person's own baseline, trends, alerts, and advice that changes with the ground-reply delay. Only the way the numbers arrive would change. Mood, social contact and food eaten would still be typed in, because no sensor measures them.

CrewPulse's advice is general guidance based on public NASA research and standards (including NASA-STD-3001). It does not replace a flight surgeon or a crew's medical protocol.