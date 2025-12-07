-- Weather Pipeline Database Schema
-- Created: Day 3
-- Database: PostgreSQL 15 on AWS RDS

-- Main observations table
CREATE TABLE IF NOT EXISTS weather_observations (
    id BIGSERIAL PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    temperature NUMERIC(5,2),
    feels_like NUMERIC(5,2),
    humidity INTEGER CHECK (humidity BETWEEN 0 AND 100),
    pressure INTEGER CHECK (pressure BETWEEN 800 AND 1200),
    wind_speed NUMERIC(5,2),
    weather_condition VARCHAR(50),
    weather_description TEXT,
    data_quality_score NUMERIC(3,2) DEFAULT 1.0,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    
    -- Prevent duplicate entries
    CONSTRAINT unique_city_timestamp UNIQUE(city, timestamp)
);

-- Indexes for query performance
CREATE INDEX IF NOT EXISTS idx_city_timestamp 
    ON weather_observations(city, timestamp DESC);

CREATE INDEX IF NOT EXISTS idx_timestamp 
    ON weather_observations(timestamp DESC);

CREATE INDEX IF NOT EXISTS idx_quality_score 
    ON weather_observations(data_quality_score) 
    WHERE data_quality_score < 0.8;

-- Comments for documentation
COMMENT ON TABLE weather_observations IS 
    'Real-time weather observations collected every 15 minutes';

COMMENT ON COLUMN weather_observations.data_quality_score IS 
    'Data quality score from 0.0 to 1.0 based on validation rules';

COMMENT ON COLUMN weather_observations.timestamp IS 
    'UTC timestamp when weather observation was recorded';

-- View for latest observations per city
CREATE OR REPLACE VIEW latest_weather AS
SELECT DISTINCT ON (city)
    city,
    timestamp,
    temperature,
    feels_like,
    humidity,
    pressure,
    wind_speed,
    weather_condition,
    weather_description,
    data_quality_score
FROM weather_observations
ORDER BY city, timestamp DESC;

COMMENT ON VIEW latest_weather IS 
    'Most recent weather observation for each city';

