"""backend/sources.py: every source used anywhere in the app. Indicators and hazards refer to these by id.

tier = "primary"   -> agency, standards body or medical guideline body
tier = "secondary" -> news site or explainer; confirm against a primary source before final submission
"""

ACCESSED = "2026-11-14"

SOURCES = {
    "nasa_hazards": {
        "title": "NASA Human Research Program: Hazards", "publisher": "NASA", "tier": "primary",
        "url": "https://www.nasa.gov/hrp/hazards", "used_for": "The five hazards of human spaceflight"},
    "nasa_risks": {
        "title": "NASA Human Research Program: Risks", "publisher": "NASA", "tier": "primary",
        "url": "https://www.nasa.gov/hrp/risks", "used_for": "Health risks that follow from the hazards"},
    "nasa_hrr": {
        "title": "Human Research Roadmap", "publisher": "NASA", "tier": "primary",
        "url": "https://humanresearchroadmap.nasa.gov/", "used_for": "Detailed risk database (look up a risk in depth)"},
    "pmc_red_risks": {
        "title": "Red risks for a journey to the red planet", "publisher": "NASA authors, PubMed Central", "tier": "primary",
        "url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC7645687", "used_for": "Highest-priority spaceflight health risks"},
    "nasa_radiation_brief": {
        "title": "Radiation Protection Technical Brief (OCHMO-TB-020)", "publisher": "NASA", "tier": "primary",
        "url": "https://www.nasa.gov/wp-content/uploads/2023/03/radiation-protection-technical-brief-ochmo.pdf",
        "used_for": "NASA career limit of 600 mSv, universal for all ages and sexes (NASA-STD-3001 Vol 1 Rev B)"},
    "nasa_exercise": {
        "title": "Astronaut Exercise", "publisher": "NASA", "tier": "primary",
        "url": "https://www.nasa.gov/missions/station/iss-research/astronaut-exercise",
        "used_for": "ISS crew average about two hours of exercise a day (resistive device, treadmill, cycle)"},
    "nas_radiation": {
        "title": "NASA should update astronaut radiation exposure limits", "publisher": "National Academies", "tier": "primary",
        "url": "https://www.nationalacademies.org/news/nasa-should-update-astronaut-radiation-exposure-limits-improve-communication-of-cancer-risks",
        "used_for": "Recommended universal career limit of about 600 mSv"},
    "space_radiation": {
        "title": "Why does NASA let male astronauts stay in space longer than females?", "publisher": "Space.com", "tier": "secondary",
        "url": "https://www.space.com/why-astronauts-radiation-levels",
        "used_for": "ISS about 300 mSv per year; Mars trip about 900 mSv (older sex and age limits there are outdated)"},
    "space_mars_risks": {
        "title": "From Radiation to Isolation: 5 Big Risks for Mars Astronauts", "publisher": "Space.com", "tier": "secondary",
        "url": "https://www.space.com/42918-big-space-risks-mars-astronauts-videos.html",
        "used_for": "Mars-Earth communication delay of about 20 minutes each way"},
    "aha_bp": {
        "title": "Top 10 Things to Know About the AHA/ACC High Blood Pressure Guideline", "publisher": "American Heart Association", "tier": "primary",
        "url": "https://www.heart.org/en/health-topics/high-blood-pressure/the-facts-about-high-blood-pressure/high-bp-top-10",
        "used_for": "Blood pressure categories (normal under 120/80; stage 1 from 130/80; stage 2 from 140/90)"},
    "mayo_low_bp": {
        "title": "Low blood pressure (hypotension)", "publisher": "Mayo Clinic", "tier": "primary",
        "url": "https://www.mayoclinic.org/diseases-conditions/low-blood-pressure/symptoms-causes/syc-20355465",
        "used_for": "Low blood pressure is generally below 90/60"},
    "livescience_bp": {
        "title": "What is normal blood pressure?", "publisher": "Live Science", "tier": "secondary",
        "url": "https://www.livescience.com/42219-blood-pressure.html", "used_for": "Low blood pressure usually below 90/60"},
    "mayo_hr": {
        "title": "Heart rate: What's normal?", "publisher": "Mayo Clinic", "tier": "primary",
        "url": "https://www.mayoclinic.org/healthy-lifestyle/fitness/expert-answers/heart-rate/faq-20057979",
        "used_for": "Normal adult resting heart rate of 60-100 bpm"},
    "cdc_sleep": {
        "title": "FastStats: Sleep in Adults", "publisher": "CDC", "tier": "primary",
        "url": "https://www.cdc.gov/Sleep/Data-Research/Facts-Stats/Adults-Sleep-Facts-And-Stats.Html",
        "used_for": "Recommended adult sleep of at least 7 hours"},
    "sleep_foundation": {
        "title": "How much sleep do we really need?", "publisher": "Sleep Foundation", "tier": "secondary",
        "url": "https://www.sleepfoundation.org/physical-health/how-much-sleep-do-we-really-need",
        "used_for": "Most healthy adults need 7 to 9 hours (cites AASM and SRS)"},
    "medlineplus_temp": {
        "title": "Body temperature norms", "publisher": "MedlinePlus (US National Library of Medicine)", "tier": "primary",
        "url": "https://nlm.nih.gov/medlineplus/ency/article/001982.htm",
        "used_for": "Normal 36.1-37.2 C; fever above 38 C"},
    "cdc_glucose": {
        "title": "Diabetes Tests", "publisher": "CDC", "tier": "primary",
        "url": "https://www.cdc.gov/diabetes/diabetes-testing/index.html",
        "used_for": "Fasting blood sugar: normal 99 or lower, prediabetes 100-125, diabetes 126 or higher"},
    "cdc_low_glucose": {
        "title": "Low Blood Sugar (Hypoglycemia)", "publisher": "CDC", "tier": "primary",
        "url": "https://cdc.gov/diabetes/about/low-blood-sugar-hypoglycemia.html",
        "used_for": "Low blood sugar is below 70 mg/dL; severe low is below 54"},
    "csa_astroskin": {
        "title": "Bio-Monitor: Keeping an eye on astronauts' vital signs", "publisher": "Canadian Space Agency", "tier": "primary",
        "url": "https://www.asc-csa.gc.ca/eng/sciences/astroskin.asp", "used_for": "Existing wearable health monitor on the ISS"},
    "nasa_mda": {
        "title": "Medical Data Architecture, Test Bed 1", "publisher": "NASA NTRS", "tier": "primary",
        "url": "https://ntrs.nasa.gov/api/citations/20170000744/downloads/20170000744.pdf",
        "used_for": "Existing NASA crew medical data system for delayed communications"},
}


def link(source_id):
    s = SOURCES[source_id]
    return f"[{s['publisher']}: {s['title']}]({s['url']})"