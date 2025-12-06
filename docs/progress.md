# Project Progress Log

## Day 1 (Dec 4, 2024)
- Initialized Git repository
- Created project structure
- Overcame the starting barrier

## Day 2 (Dec 5, 2024)
**Goal:** Get real weather data from API

**Accomplished:**
- ✅ Set up Python virtual environment
- ✅ Obtained OpenWeatherMap API key
- ✅ Built API test script
- ✅ Successfully pulled weather data for 5 cities
- ✅ Explored API response structure
- ✅ Identified data fields for database schema

**Key Learnings:**
- OpenWeatherMap API is straightforward, good documentation
- Response includes more data than needed (can select specific fields)
- Free tier: 60 calls/minute, 1000 calls/day (plenty for our needs)

**Data Fields Identified for Database:**
- city (varchar)
- timestamp (timestamptz)
- temperature (numeric)
- feels_like (numeric)
- humidity (integer)
- pressure (integer)
- wind_speed (numeric)
- weather_condition (varchar)
- weather_description (text)

**Next Steps (Day 3):**
- Set up AWS RDS PostgreSQL database
- Design production schema with indexes
- Connect Python to RDS

**Blockers:** None

**Time Invested:** 1 hours
