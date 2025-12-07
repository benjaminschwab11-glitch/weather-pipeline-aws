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

## Day 3 (Dec 6, 2024)
**Goal:** Deploy AWS RDS PostgreSQL database with production schema

**Accomplished:**
- ✅ Created RDS PostgreSQL instance (db.t4g.micro, free tier)
- ✅ Configured security group for secure access
- ✅ Tested database connection successfully
- ✅ Designed production schema with:
  - weather_observations table
  - Data quality constraints
  - Performance indexes (city, timestamp)
  - latest_weather view for quick queries
- ✅ Deployed schema to RDS
- ✅ Verified tables, indexes, and views created

**Key Decisions:**
- Used PostgreSQL over DynamoDB (leverages SQL expertise)
- Implemented data quality score field (proactive monitoring)
- Created compound index on (city, timestamp DESC) for dashboard queries
- Added unique constraint to prevent duplicate records

**Estimated Monthly Cost:** $15 (within free tier for first 12 months)

**Next Steps (Day 4):**
- Connect API collector to RDS
- Insert first real weather data
- Verify data quality checks work

**Time Invested:** 1.5 hours
