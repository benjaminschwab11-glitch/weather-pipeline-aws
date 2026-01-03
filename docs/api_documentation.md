# Weather Data API Documentation

**Base URL:** `https://v7x2axj6u9.execute-api.us-west-2.amazonaws.com/prod`  
**Version:** 1.0  
**Deployed:** January 2, 2026

## Overview

REST API providing programmatic access to real-time and historical weather data collected from 5 West Coast cities. Data updated every 15 minutes via automated pipeline.

## Authentication

**Current:** Public API, no authentication required  
**Future:** API key authentication recommended for production

## Endpoints

### 1. Get Current Weather

**Endpoint:** `GET /weather`

**Description:** Returns the most recent weather observation for all cities or a specific city.

**Query Parameters:**
- `city` (optional): Filter by city name (e.g., "San Diego")

**Example Requests:**
```bash
# All cities
curl https://v7x2axj6u9.execute-api.us-west-2.amazonaws.com/prod/weather

# Specific city
curl "https://v7x2axj6u9.execute-api.us-west-2.amazonaws.com/prod/weather?city=San%20Diego"
```

**Example Response:**
```json
{
  "count": 5,
  "data": [
    {
      "city": "San Diego",
      "timestamp": "2026-01-02T00:15:23.456789+00:00",
      "temperature": 64.7,
      "feels_like": 63.2,
      "humidity": 72,
      "pressure": 1013,
      "wind_speed": 8.5,
      "weather_condition": "Clouds",
      "weather_description": "broken clouds",
      "data_quality_score": 1.0
    },
    ...
  ]
}
```

---

### 2. Get Weather History

**Endpoint:** `GET /weather/history`

**Description:** Returns historical weather observations within a specified time range.

**Query Parameters:**
- `city` (optional): Filter by city name
- `hours` (optional): Hours of history to retrieve (default: 24, max: 168)
- `limit` (optional): Maximum records to return (default: 100, max: 1000)

**Example Requests:**
```bash
# Last 24 hours, all cities
curl "https://v7x2axj6u9.execute-api.us-west-2.amazonaws.com/prod/weather/history?hours=24&limit=50"

# Last 48 hours, specific city
curl "https://v7x2axj6u9.execute-api.us-west-2.amazonaws.com/prod/weather/history?city=Seattle&hours=48&limit=100"
```

**Example Response:**
```json
{
  "count": 50,
  "hours": 24,
  "data": [
    {
      "city": "Los Angeles",
      "timestamp": "2026-01-02T00:00:00+00:00",
      "temperature": 65.3,
      "feels_like": 64.1,
      "humidity": 68,
      "pressure": 1012,
      "wind_speed": 7.2,
      "weather_condition": "Clear",
      "weather_description": "clear sky",
      "data_quality_score": 1.0
    },
    ...
  ]
}
```

---

### 3. Get Quality Metrics

**Endpoint:** `GET /quality`

**Description:** Returns data quality metrics aggregated per collection run.

**Query Parameters:**
- `hours` (optional): Hours of metrics to retrieve (default: 24)

**Example Request:**
```bash
curl "https://v7x2axj6u9.execute-api.us-west-2.amazonaws.com/prod/quality?hours=48"
```

**Example Response:**
```json
{
  "count": 192,
  "hours": 48,
  "data": [
    {
      "collection_timestamp": "2026-01-02T00:15:00+00:00",
      "total_records": 5,
      "perfect_quality_count": 5,
      "degraded_quality_count": 0,
      "failed_quality_count": 0,
      "avg_quality_score": 1.0,
      "min_quality_score": 1.0,
      "max_quality_score": 1.0,
      "temperature_failures": 0,
      "humidity_failures": 0,
      "pressure_failures": 0,
      "wind_speed_failures": 0
    },
    ...
  ]
}
```

---

## Response Format

**Success Response:**
- **Status Code:** 200
- **Content-Type:** application/json
- **Body:** JSON object with `count` and `data` fields

**Error Response:**
- **Status Code:** 404 (Not Found) or 500 (Internal Server Error)
- **Content-Type:** application/json
- **Body:** JSON object with `error` and `message` fields

**Example Error:**
```json
{
  "error": "Not Found",
  "message": "Endpoint /invalid not found"
}
```

---

## Data Schema

### Weather Observation

| Field | Type | Description | Example |
|-------|------|-------------|---------|
| city | string | City name | "San Diego" |
| timestamp | datetime | Observation timestamp (UTC) | "2026-01-02T00:15:00Z" |
| temperature | float | Temperature (°F) | 64.7 |
| feels_like | float | Feels like temperature (°F) | 63.2 |
| humidity | integer | Humidity (%) | 72 |
| pressure | integer | Atmospheric pressure (hPa) | 1013 |
| wind_speed | float | Wind speed (mph) | 8.5 |
| weather_condition | string | General condition | "Clouds" |
| weather_description | string | Detailed description | "broken clouds" |
| data_quality_score | float | Quality score (0.0-1.0) | 1.0 |

### Quality Metrics

| Field | Type | Description |
|-------|------|-------------|
| collection_timestamp | datetime | Collection run timestamp |
| total_records | integer | Total records in collection |
| perfect_quality_count | integer | Records with score = 1.0 |
| degraded_quality_count | integer | Records with 0.7 ≤ score < 1.0 |
| failed_quality_count | integer | Records with score < 0.7 |
| avg_quality_score | float | Average quality score |
| min_quality_score | float | Minimum quality score |
| max_quality_score | float | Maximum quality score |
| temperature_failures | integer | Temperature validation failures |
| humidity_failures | integer | Humidity validation failures |
| pressure_failures | integer | Pressure validation failures |
| wind_speed_failures | integer | Wind speed validation failures |

---

## CORS Support

All endpoints support Cross-Origin Resource Sharing (CORS) with:
- **Access-Control-Allow-Origin:** `*`
- **Access-Control-Allow-Methods:** GET, OPTIONS
- **Access-Control-Allow-Headers:** Content-Type

---

## Rate Limiting

**Current:** No rate limiting  
**Recommended:** 100 requests/minute per IP for production

---

## Cities Tracked

1. San Diego, CA
2. Los Angeles, CA
3. San Francisco, CA
4. Seattle, WA
5. Portland, OR

---

## Data Collection Frequency

- **Collection interval:** Every 15 minutes
- **Records per day:** ~480 (96 collections × 5 cities)
- **Data retention:** All historical data retained

---

## Use Cases

**Real-time Monitoring:**
```bash
# Get current conditions
curl https://v7x2axj6u9.execute-api.us-west-2.amazonaws.com/prod/weather
```

**Trend Analysis:**
```bash
# Get last week of data
curl "https://v7x2axj6u9.execute-api.us-west-2.amazonaws.com/prod/weather/history?hours=168&limit=1000"
```

**Quality Monitoring:**
```bash
# Check data quality over last 24 hours
curl "https://v7x2axj6u9.execute-api.us-west-2.amazonaws.com/prod/quality?hours=24"
```

**City-Specific Tracking:**
```bash
# Seattle weather history
curl "https://v7x2axj6u9.execute-api.us-west-2.amazonaws.com/prod/weather/history?city=Seattle&hours=48"
```

---

## Technical Implementation

**Architecture:**
- **API Gateway:** REST API with regional endpoint
- **Lambda:** Python 3.11 function (`weather-api`)
- **Database:** RDS PostgreSQL
- **Security:** TLS 1.3, CORS enabled

**Performance:**
- **Response time:** <500ms typical
- **Cold start:** ~600ms
- **Concurrent requests:** Up to AWS Lambda limits

---

## Future Enhancements

**Planned:**
- [ ] API key authentication
- [ ] Rate limiting
- [ ] Response caching
- [ ] Additional query filters (date ranges, temperature ranges)
- [ ] WebSocket support for real-time updates
- [ ] Pagination for large result sets
- [ ] OpenAPI/Swagger documentation
- [ ] GraphQL endpoint

---

## Contact & Support

**API Issues:** Check CloudWatch logs for Lambda function `weather-api`  
**GitHub:** https://github.com/benjaminschwab11-glitch/weather-pipeline-aws  
**Dashboard:** https://weather-pipeline-aws-f2ov36k74bnjfmhmcvbikw.streamlit.app

---

## Changelog

**v1.0 (2026-01-02):**
- Initial API release
- Three GET endpoints
- JSON responses
- CORS support
- Quality metrics endpoint

