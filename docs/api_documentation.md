# Weather Data API Documentation

**Base URL:** `https://v7x2axj6u9.execute-api.us-west-2.amazonaws.com/prod`  
**Version:** 1.0  
**Deployed:** January 2, 2026

## Overview

REST API providing programmatic access to real-time weather data, historical trends, quality metrics, and GDPR/CCPA compliance endpoints.

## Authentication

**Current:** Public API, no authentication required  
**Future:** API key authentication recommended for production

## Endpoints

1. **GET /weather** - Current weather data
2. **GET /weather/history** - Historical weather data
3. **GET /quality** - Quality metrics
4. **POST /compliance/consent** - Record user consent
5. **GET /compliance/consent** - Get user consents
6. **POST /compliance/dsar** - Create data subject request
7. **GET /compliance/export** - Export user data

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

### 4. Record User Consent

**Endpoint:** `POST /compliance/consent`

**Description:** Records user consent for data processing activities (GDPR/CCPA compliance).

**Request Body:**
```json
{
  "user_id": "string (required)",
  "consent_type": "string (required)",
  "granted": "boolean (required)",
  "version": "string (optional, default: '1.0')"
}
```

**Consent Types:**
- `DATA_PROCESSING` - General data processing
- `MARKETING` - Marketing communications
- `ANALYTICS` - Analytics and tracking
- `THIRD_PARTY_SHARING` - Sharing with third parties

**Example Request:**
```bash
curl -X POST https://v7x2axj6u9.execute-api.us-west-2.amazonaws.com/prod/compliance/consent \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "consent_type": "MARKETING",
    "granted": true
  }'
```

**Example Response:**
```json
{
  "consent_id": 42,
  "message": "Consent recorded"
}
```

---

### 5. Get User Consents

**Endpoint:** `GET /compliance/consent`

**Description:** Retrieves all consent records for a specific user.

**Query Parameters:**
- `user_id` (required): User identifier

**Example Request:**
```bash
curl "https://v7x2axj6u9.execute-api.us-west-2.amazonaws.com/prod/compliance/consent?user_id=user_123"
```

**Example Response:**
```json
{
  "user_id": "user_123",
  "consents": [
    {
      "consent_type": "MARKETING",
      "consent_granted": true,
      "consent_timestamp": "2026-01-06T04:30:00+00:00",
      "consent_version": "1.0",
      "consent_status": "ACTIVE"
    },
    {
      "consent_type": "ANALYTICS",
      "consent_granted": false,
      "consent_timestamp": "2026-01-06T04:25:00+00:00",
      "consent_version": "1.0",
      "consent_status": "ACTIVE"
    }
  ]
}
```

---

### 6. Create DSAR Request

**Endpoint:** `POST /compliance/dsar`

**Description:** Creates a Data Subject Access Request (GDPR Article 15, CCPA §1798.100).

**Request Body:**
```json
{
  "user_id": "string (required)",
  "request_type": "string (required)",
  "requester_email": "string (optional)"
}
```

**Request Types:**
- `ACCESS` - Right to access personal data
- `DELETION` - Right to be forgotten/deleted
- `RECTIFICATION` - Right to correct inaccurate data
- `PORTABILITY` - Right to receive data in portable format

**Example Request:**
```bash
curl -X POST https://v7x2axj6u9.execute-api.us-west-2.amazonaws.com/prod/compliance/dsar \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "request_type": "ACCESS",
    "requester_email": "user123@example.com"
  }'
```

**Example Response:**
```json
{
  "request_id": "a2dc4a01-356f-4f91-88db-ea45694c76f6",
  "message": "ACCESS request created",
  "status": "PENDING"
}
```

**SLA:** Requests are tracked with 30-day completion target per GDPR requirements.

---

### 7. Export User Data

**Endpoint:** `GET /compliance/export`

**Description:** Exports all user data in JSON format (GDPR Article 20 - Data Portability).

**Query Parameters:**
- `user_id` (required): User identifier

**Example Request:**
```bash
curl "https://v7x2axj6u9.execute-api.us-west-2.amazonaws.com/prod/compliance/export?user_id=user_123"
```

**Example Response:**
```json
{
  "user_id": "user_123",
  "export_timestamp": "2026-01-06T04:35:00.123456",
  "data_categories": {
    "consents": [
      {
        "consent_type": "MARKETING",
        "granted": true,
        "timestamp": "2026-01-06T04:30:00",
        "version": "1.0"
      }
    ],
    "dsar_requests": [
      {
        "request_id": "a2dc4a01-356f-4f91-88db-ea45694c76f6",
        "type": "ACCESS",
        "status": "COMPLETED",
        "timestamp": "2026-01-06T04:31:00"
      }
    ],
    "weather_preferences": []
  }
}
```

**Response Headers:**
```
Content-Type: application/json
Content-Disposition: attachment; filename=user_data_user_123.json
```

---

## Compliance Features

### GDPR Compliance

**Article 6 - Lawful Processing:**
- Consent management with versioning
- Audit trail of all consent changes
- Withdrawal of consent supported

**Article 15 - Right to Access:**
- DSAR request creation and tracking
- Complete data export in JSON format
- 30-day completion SLA

**Article 17 - Right to be Forgotten:**
- DSAR deletion request type
- Hard delete or anonymization options
- Complete audit trail

**Article 20 - Data Portability:**
- Machine-readable JSON export
- All user data in single response
- Structured format for easy import

### CCPA Compliance

**§1798.100 - Consumer Rights:**
- Know what personal information is collected
- Export functionality provides transparency

**§1798.105 - Right to Delete:**
- Deletion requests tracked and executed
- Verification process supported

**§1798.110 - Right to Know:**
- Complete disclosure via export endpoint
- Categories of data clearly organized

### Audit Trail

All compliance operations are logged to `audit_log` table:
- Consent changes (CONSENT_CHANGE)
- DSAR requests (DSAR_REQUEST)
- Data exports (DATA_EXPORT)
- Data deletions (DATA_DELETION)

**Query audit log:**
```sql
SELECT * FROM audit_log 
WHERE event_type IN ('CONSENT_CHANGE', 'DSAR_REQUEST')
ORDER BY event_timestamp DESC;
```

### Request Tracking

**Pending requests view:**
```sql
SELECT * FROM pending_dsar_requests;
```

**Returns:**
- Request ID and type
- Days pending
- SLA status (ON_TIME, WARNING, OVERDUE)

### Security Considerations

**Authentication:** 
- Production should require API key or OAuth
- User identity verification required for DSAR

**Rate Limiting:**
- Recommended: 10 requests/hour per user
- Prevents abuse of compliance endpoints

**Data Deletion:**
- Two modes: Hard delete (permanent) or Anonymize (preserve analytics)
- Irreversible operation - requires confirmation
- Complete audit trail maintained

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

