-- Quality Metrics Tracking Table
-- Stores quality metrics aggregated by collection run

CREATE TABLE IF NOT EXISTS quality_metrics (
    id SERIAL PRIMARY KEY,
    collection_timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    total_records INTEGER NOT NULL,
    perfect_quality_count INTEGER NOT NULL,
    degraded_quality_count INTEGER NOT NULL,
    failed_quality_count INTEGER NOT NULL,
    avg_quality_score DECIMAL(3,2) NOT NULL,
    min_quality_score DECIMAL(3,2) NOT NULL,
    max_quality_score DECIMAL(3,2) NOT NULL,
    temperature_failures INTEGER DEFAULT 0,
    humidity_failures INTEGER DEFAULT 0,
    pressure_failures INTEGER DEFAULT 0,
    wind_speed_failures INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_collection_timestamp UNIQUE(collection_timestamp)
);

-- Index for time-based queries
CREATE INDEX idx_quality_collection_timestamp ON quality_metrics(collection_timestamp DESC);

-- Index for quality score queries
CREATE INDEX idx_quality_avg_score ON quality_metrics(avg_quality_score);

-- Comments
COMMENT ON TABLE quality_metrics IS 'Aggregated data quality metrics per collection run';
COMMENT ON COLUMN quality_metrics.collection_timestamp IS 'Timestamp of the weather data collection run';
COMMENT ON COLUMN quality_metrics.perfect_quality_count IS 'Records with quality score = 1.0';
COMMENT ON COLUMN quality_metrics.degraded_quality_count IS 'Records with quality score between 0.7 and 0.99';
COMMENT ON COLUMN quality_metrics.failed_quality_count IS 'Records with quality score < 0.7';

-- Quality threshold view for alerts
CREATE OR REPLACE VIEW quality_alerts AS
SELECT 
    collection_timestamp,
    avg_quality_score,
    total_records,
    failed_quality_count,
    CASE 
        WHEN avg_quality_score < 0.7 THEN 'CRITICAL'
        WHEN avg_quality_score < 0.9 THEN 'WARNING'
        ELSE 'HEALTHY'
    END as alert_level
FROM quality_metrics
WHERE collection_timestamp >= NOW() - INTERVAL '24 hours'
ORDER BY collection_timestamp DESC;

COMMENT ON VIEW quality_alerts IS 'Quality alerts for the last 24 hours';

