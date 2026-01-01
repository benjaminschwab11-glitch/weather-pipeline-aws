# Data Quality Framework

**Implemented:** January 1, 2026  
**Status:** Production - Active Monitoring

## Overview

Comprehensive data quality framework that validates incoming weather data, tracks quality metrics over time, and provides alerts for quality degradation.

## Quality Scoring System

**Score Range:** 0.0 to 1.0

### Validation Rules

**Temperature (-50°F to 150°F):**
- Out of range: -0.3 penalty
- Rationale: Physical limits for Earth's atmosphere

**Humidity (0% to 100%):**
- Out of range: -0.3 penalty
- Rationale: Percentage cannot exceed bounds

**Pressure (900 to 1100 hPa):**
- Out of range: -0.3 penalty
- Rationale: Normal atmospheric pressure range at sea level

**Wind Speed (0 to 200 mph):**
- Negative or >200: -0.1 penalty
- Rationale: Negative impossible, >200 mph extremely rare

### Quality Thresholds

**Perfect Quality (1.0):**
- All fields within valid ranges
- No data anomalies detected

**Degraded Quality (0.7 - 0.99):**
- Minor issues detected
- Data usable but flagged for review

**Failed Quality (<0.7):**
- Multiple validation failures
- Data questionable, requires investigation

## Database Schema

### quality_metrics Table
```sql
CREATE TABLE quality_metrics (
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
```

### quality_alerts View
```sql
CREATE VIEW quality_alerts AS
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
```

## Metrics Collection

**Per Collection Run (every 15 minutes):**
- Total records collected
- Perfect quality count (score = 1.0)
- Degraded quality count (0.7 ≤ score < 1.0)
- Failed quality count (score < 0.7)
- Average quality score
- Min/max quality scores
- Failure counts by field type

**Aggregation:**
- Stored per collection timestamp
- Enables time-series analysis
- Supports trend detection

## Quality Monitoring Queries

### Current Quality Status
```sql
SELECT 
    collection_timestamp,
    total_records,
    perfect_quality_count,
    avg_quality_score,
    ROUND(100.0 * perfect_quality_count / total_records, 1) as perfect_pct
FROM quality_metrics
ORDER BY collection_timestamp DESC
LIMIT 10;
```

### Quality Trend (Last 24 Hours)
```sql
SELECT 
    DATE_TRUNC('hour', collection_timestamp) as hour,
    COUNT(*) as collections,
    AVG(avg_quality_score) as avg_score,
    MIN(min_quality_score) as worst_score,
    SUM(failed_quality_count) as total_failures
FROM quality_metrics
WHERE collection_timestamp >= NOW() - INTERVAL '24 hours'
GROUP BY DATE_TRUNC('hour', collection_timestamp)
ORDER BY hour DESC;
```

### Failure Analysis
```sql
SELECT 
    SUM(temperature_failures) as temp_fails,
    SUM(humidity_failures) as humidity_fails,
    SUM(pressure_failures) as pressure_fails,
    SUM(wind_speed_failures) as wind_fails,
    COUNT(*) as total_collections
FROM quality_metrics
WHERE collection_timestamp >= NOW() - INTERVAL '7 days';
```

### Quality Alerts
```sql
SELECT * FROM quality_alerts
WHERE alert_level IN ('WARNING', 'CRITICAL');
```

## Performance Baselines

**Expected Performance:**
- Average quality score: 0.95+
- Perfect quality rate: >90%
- Failed quality count: 0 per collection
- Alert level: HEALTHY

**Historical Performance (Since Implementation):**
- Average quality score: 1.00
- Perfect quality rate: 100%
- Zero quality failures recorded
- Consistent HEALTHY status

## Alert Response Procedures

### WARNING Alert (avg_quality_score < 0.9)

**Actions:**
1. Check quality_metrics for failure patterns
2. Review recent collection logs
3. Verify API response quality
4. Monitor for 1 hour
5. Escalate if persists

### CRITICAL Alert (avg_quality_score < 0.7)

**Actions:**
1. Immediate log review
2. Check API service status
3. Verify database connectivity
4. Review failure breakdown by field
5. Consider pausing collection if sustained

## Quality Improvements Implemented

**Original System:**
- Quality scoring per record
- Stored in weather_observations table
- No aggregation or trending

**Enhanced System:**
- Aggregated metrics per collection
- Dedicated quality_metrics table
- Alert view for quick status check
- Failure tracking by validation type
- Time-series analysis capability

## Data Contracts

### Input Expectations (OpenWeatherMap API)

**Required Fields:**
- main.temp (temperature)
- main.feels_like
- main.humidity (0-100)
- main.pressure (hPa)
- wind.speed (mph)
- weather[0].main (condition)
- weather[0].description

**Quality Guarantees:**
- All fields present in API response
- Numeric fields are valid numbers
- Values within physical possibility

### Output Guarantees

**weather_observations:**
- All records have quality_score (0.0-1.0)
- Timestamp shared across collection run
- No duplicate (city, timestamp) combinations

**quality_metrics:**
- One record per collection timestamp
- Aggregated metrics match detail records
- Alert level computed consistently

## Integration Points

### Lambda Function

**Quality calculation:**
```python
def calculate_quality_metrics(self, records):
    # Aggregates individual quality scores
    # Categorizes by threshold
    # Tracks failure types
```

**Quality storage:**
```python
def store_quality_metrics(self, metrics):
    # Inserts to quality_metrics table
    # ON CONFLICT updates existing
```

### CloudWatch

**Custom Metrics Published:**
- RecordsCollected
- RecordsStored
- ExecutionTime

**Future Enhancement:**
- Add AvgQualityScore metric
- Add FailedQualityCount metric

### Streamlit Dashboard

**Current:** Shows individual record quality scores

**Future Enhancement:**
- Quality trends chart (24h, 7d, 30d)
- Quality distribution histogram
- Failure type breakdown
- Alert status indicator

## Testing

**Unit Tests:**
- Quality scoring logic (14 tests)
- Boundary value testing
- Multiple failure scenarios
- Score capping (0.0 minimum)

**Integration Testing:**
- End-to-end quality tracking
- Database storage verification
- Alert view functionality

## Future Enhancements

**Planned:**
- [ ] CloudWatch alarm on avg_quality_score < 0.9
- [ ] SNS notification for CRITICAL alerts
- [ ] Quality dashboard in Streamlit
- [ ] Automated quality reports (daily/weekly)
- [ ] Historical quality analysis (trends, patterns)
- [ ] Anomaly detection (sudden quality drops)
- [ ] Data lineage tracking

**Possible:**
- [ ] Great Expectations integration
- [ ] Custom validation rules per city
- [ ] Seasonal quality benchmarks
- [ ] ML-based quality prediction

## Interview Talking Points

**"I implemented a comprehensive data quality framework with scoring, tracking, and alerting."**

**Key Features:**
- 0.0-1.0 quality scoring per record
- Aggregated metrics per collection run
- Time-series quality tracking
- Alert view (HEALTHY/WARNING/CRITICAL)
- Failure analysis by field type
- Production deployment with monitoring

**Business Value:**
- Early detection of data issues
- Trend analysis over time
- Automated alerting (future)
- Data governance compliance
- Trust in pipeline outputs

**Technical Depth:**
- Database schema design
- Aggregate calculations
- SQL view creation
- Lambda integration
- Error handling and rollback


