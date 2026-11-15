# CrewPulse research file

This file records where every number and claim in CrewPulse came from, how reliable each source is, and what the project does not cover.
All sources were opened and checked on 2026-11-13, 2026-11-14 and 2026-11-15. A ticked box in the Verified column means the number was confirmed on the source page.

## 1. Source reliability ranking

Sources are ranked from most to least reliable. Every source used in CrewPulse is listed below under the group it belongs to, and the same list appears with links in the app's Guide page.

1. **Space agencies and their researchers (used for anything astronaut-specific):**
   - NASA Human Research Program: hazards and risks pages
   - NASA Human Spaceflight Standards, NASA-STD-3001 (Office of the Chief Health and Medical Officer): the Agency standard for crew health and medical care (Volume 1) and human factors and environmental health (Volume 2)
   - NASA Radiation Protection Technical Brief (career limit of 600 mSv)
   - NASA: Astronaut Exercise
   - NASA Technical Reports Server: Medical Data Architecture, Test Bed 1
   - Canadian Space Agency: Bio-Monitor (Astroskin)
   - PubMed Central: "Red risks for a journey to the red planet" (NASA authors)
2. **National Academies of Sciences, Engineering, and Medicine:** the recommendation to update NASA's astronaut radiation limit.
3. **Medical bodies (used for normal ranges for healthy adults on Earth):** American Heart Association (blood pressure), Mayo Clinic (heart rate, low blood pressure), CDC (sleep, blood sugar) and MedlinePlus (body temperature).
4. **News and explainers (used for context only):** Space.com (radiation figures, Mars communication delay), Sleep Foundation (7 to 9 hours of sleep) and Live Science (low blood pressure).

When sources disagreed, the higher-ranked one was used. For example, Space.com gives older radiation limits that vary by age and sex, while NASA's technical brief gives a single 600 mSv limit, so the app uses NASA's.

Any number without a source is labelled "app design" in the app and in section 3 below.

## 2. The five hazards (NASA Human Research Program)

| Hazard | In the app | Source |
|---|---|---|
| Space radiation | Cumulative dose as % of career limit | nasa.gov/hrp/hazards |
| Isolation and confinement | Mood, sleep, social contact | nasa.gov/hrp/hazards |
| Distance from Earth | Ground reply delay changes the advice (autonomous mode) | nasa.gov/hrp/hazards |
| Gravity fields | Heart rate, blood pressure, resistive exercise | nasa.gov/hrp/hazards |
| Hostile closed environment | Temperature, glucose, food eaten | nasa.gov/hrp/hazards |

Related reading: nasa.gov/hrp/risks (risks that follow from the hazards); PMC7645687 "Red risks for a journey to the red planet"; nasa.gov/hrp/ongoing-hrp-research (NASA's list of current human research studies, including Standard Measures, which collects physiological and psychological measurements from crews).

## 3. Indicators, ranges and sources

| Indicator | Normal | Watch | Basis | Source | Tier | Verified |
|---|---|---|---|---|---|---|
| Resting heart rate | 60-100 bpm | 50-110 | Mayo Clinic: 60-100 normal; watch margin is app design | mayoclinic.org (heart-rate FAQ) | primary | [x] |
| Blood pressure, top | 90-119 mmHg | 85-139 | AHA: normal under 120, stage 1 from 130, stage 2 from 140; Mayo Clinic: low is below 90; 85 is app margin | heart.org high-bp-top-10; mayoclinic.org low-blood-pressure | primary | [x] |
| Blood pressure, bottom | 60-79 mmHg | 55-89 | AHA: normal under 80, stage 1 from 80, stage 2 from 90; Mayo Clinic: low is below 60; 55 is app margin | heart.org high-bp-top-10; mayoclinic.org low-blood-pressure | primary | [x] |
| Sleep | 7-9 h | 6-10 | CDC: at least 7 h; 7-9 h from Sleep Foundation (secondary); watch margin 6-10 is app design | cdc.gov Sleep FastStats; sleepfoundation.org | primary / secondary | [x] |
| Body temperature | 36.1-37.2 C | 35.5-38.0 | MedlinePlus: normal 36.1-37.2, fever above 38; 35.5 is app margin | nlm.nih.gov MedlinePlus | primary | [x] |
| Fasting glucose | 70-99 mg/dL | 60-125 | CDC: normal 99 or lower, prediabetes 100-125, diabetes 126+; CDC: low is below 70, severe low below 54; 60 is app margin | cdc.gov diabetes-testing; cdc.gov low-blood-sugar | primary | [x] |
| Radiation | 0-50% of 600 mSv | 0-80% | NASA career limit is 600 mSv, universal for all ages and sexes (NASA technical brief, 2022; National Academies recommended it in 2021); 50% and 80% steps are app design | nasa.gov radiation technical brief; nationalacademies.org | primary | [x] |
| Mood, social contact, food eaten | n/a | n/a | App design (self-reported scales) | none | design | n/a |
| Resistive exercise | 60+ min/day | 30+ | App design targets. Context: NASA says ISS crew average about 2 hours of exercise a day (resistive, treadmill, cycle) | nasa.gov astronaut-exercise | primary (context only) | n/a |

Radiation context (Space.com, secondary, partly outdated): ISS about 300 mSv per year versus about 3.6 mSv on Earth; Mars mission about 900 mSv. Space.com's older limits of 180-700 mSv by age and sex were replaced by NASA's single 600 mSv limit (NASA technical brief, December 2022).

## 4. Existing systems

- **Astroskin / Bio-Monitor** (Canadian Space Agency, Hexoskin): a smart shirt measuring heart, blood pressure, respiration, skin temperature and activity; used on the ISS.
  Source: asc-csa.gc.ca/eng/sciences/astroskin.asp
- **NASA Medical Data Architecture, Test Bed 1:** collects device data into an electronic medical record for the Crew Medical Officer; built for delayed communications.
  Source: NTRS 20170000744
- **Gap CrewPulse targets:** these systems serve clinicians and researchers. CrewPulse is for the astronaut who is not a doctor: plain explanations, drift from the person's own baseline, and advice that changes with the ground-reply delay. This was not compared against other Space Apps entries.

## 5. Design decisions

- Watch margins around each normal range exist so the app warns before a reading becomes serious.
- Baseline is the first 14 days; a drift alert fires at 2.5 standard deviations (app design).
- Distance-from-Earth status combines the urgency of the worst alert with how slow the ground is to reply. Autonomous mode starts at 5 minutes or more one way (app design).
- The simulated mission (180 days, infection around days 112-116) only demonstrates the logic.
- Moon and Mars daily radiation figures in `backend/environments.py` are assumptions.
- Normal ranges are for healthy adults on Earth. In space, drift from a person's own baseline matters more.
- NASA-STD-3001 is the reference for what NASA treats as crew health requirements, and the 600 mSv radiation limit comes from its Volume 1 (Rev B) through NASA's technical brief. CrewPulse does not implement the standard. Its advice is general guidance written for the prototype, and in-flight emergency procedures are operational documents held by NASA flight surgeons, which are not reproduced here.

## 6. Limitations and future work

- **Exercise targets:** NASA reports that ISS crews average about 2 hours of exercise a day across all types. The 60 and 30 minute lines in the app are design targets, not NASA figures.
- **Glucose bands:** confirmed against CDC guidance for adults on Earth.
- **Radiation limit:** NASA's 600 mSv career limit is adopted (NASA technical brief, 2022).
- **Moon and Mars daily radiation doses:** the figures in `backend/environments.py` are assumptions. Sourced values for lunar surface and Mars transit are future work.
- **Routine ISS measurements:** which vital signs and tests are taken routinely in flight is not yet documented here. Adding sourced notes on this is future work.
- **Data:** all mission data in the app is simulated. No real astronaut data was used.