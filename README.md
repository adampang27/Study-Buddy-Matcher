# Smart Buddy - Study Partner Matching System

A web app that matches university students with compatible study partners. Students create a profile with their personality type, study style, academic focus areas, and weekly availability. The system scores every possible pairing across those four factors and ranks the best matches. It also handles scheduling by finding overlapping free time between matched partners.

> **Live Demo:** [https://smart-buddy-matcher.onrender.com](https://smart-buddy-matcher.onrender.com)

## How It Works

1. A student signs up and fills out a profile (personality type, study style, preferred environment, academic focus areas, availability).
2. The matching engine scores them against every other student in the system using four weighted factors.
3. Results are ranked by overall compatibility, and the app suggests study session times based on shared availability.

## Matching Algorithm

The compatibility engine scores each pair of students across four dimensions, each weighted at 25%:

| Factor | How It's Scored |
|--------|----------------|
| **Personality** | Same type = 100, Ambivert match = 85, Introvert/Extrovert = 70 |
| **Study Style** | Compares group vs. individual vs. mixed preferences |
| **Academic Goals** | Jaccard similarity on overlapping focus areas |
| **Availability** | Percentage of shared time slots + bonus for multiple overlaps |

The final score is a weighted average of all four. Only matches above a minimum threshold (default 50) are returned.

## Scheduling (CSP Solver)

Once students are matched, a Constraint Satisfaction Problem solver finds valid study session times. It respects constraints like:

- Max 2 sessions per day per student
- Max 6 sessions per week
- Max 3 unique study partners
- Prefers weekday mornings over weekend evenings

It also has an optimization pass that tries to shift sessions to more preferred time slots after the initial schedule is built.

## Data Model

Three tables in a PostgreSQL database (MySQL for local dev):

- **Profiles** - username, email, study style, environment preference, personality traits (JSON), academic focus areas (JSON), availability (JSON)
- **Sessions** - pairs two students with a datetime and status (scheduled/completed/cancelled)
- **Ratings** - post-session peer feedback with a 1-5 score

## Tech Stack

- **Backend:** Python, FastAPI
- **Frontend:** Jinja2 templates, HTML/CSS
- **Database:** PostgreSQL (production), MySQL (local dev)
- **ORM:** SQLAlchemy
- **Validation:** Pydantic
- **Testing:** pytest
- **Deployment:** Render

## Project Structure

```
smart_buddy/
├── matching/
│   ├── compatibility_engine.py   # Weighted scoring algorithm
│   ├── matching_service.py       # Orchestrates matching + scheduling
│   └── csp_solver.py             # Constraint satisfaction scheduling
├── models/
│   └── sqlalchemy_models.py      # Database table definitions
├── routers/                      # API route handlers
├── schemas/                      # Pydantic validation schemas
├── templates/                    # Jinja2 HTML templates
├── static/                       # CSS and images
├── tests/
│   ├── test_availability_model.py
│   ├── test_availability_api.py
│   ├── test_calendar_integration.py
│   └── test_compatibility_engine.py
├── db.py                         # Database config and session management
└── main.py                       # App entry point
```

## Local Setup

```bash
git clone https://github.com/adampang27/Study-Buddy-Matcher.git
cd Study-Buddy-Matcher
pip install -r requirements.txt

# Set up your database credentials
cp .env.example .env
# Edit .env with your local MySQL credentials

# Create the database tables
python init_db.py
```

## Running Tests

```bash
python -m pytest smart_buddy/tests/ -v
```