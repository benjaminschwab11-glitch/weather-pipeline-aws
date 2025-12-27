# Testing Documentation

**Framework:** pytest  
**Coverage Tool:** pytest-cov  
**Tests Added:** December 26, 2024

## Overview

Unit tests validate core data processing and validation logic without requiring live AWS resources or API connections.

## Test Structure
```
tests/
├── __init__.py
├── conftest.py              # Shared fixtures
├── test_data_validation.py  # Data quality validation tests (8 tests)
└── test_weather_processing.py # Data transformation tests (6 tests)
```

## Running Tests

### Run All Tests
```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=src --cov-report=term-missing
```

### Run Specific Test Files
```bash
# Run only validation tests
pytest tests/test_data_validation.py -v

# Run only processing tests
pytest tests/test_weather_processing.py -v
```

### Run Specific Tests
```bash
# Run single test by name
pytest tests/test_data_validation.py::TestDataValidation::test_valid_weather_data -v

# Run tests matching pattern
pytest -k "invalid" -v
```

## Test Coverage

**Current Status:** 14 tests, 100% passing

### test_data_validation.py (8 tests)

**TestDataValidation:**
- `test_valid_weather_data` - Perfect score for valid data
- `test_invalid_temperature` - Temperature out of range detection (-50°F to 150°F)
- `test_invalid_humidity` - Humidity validation (0-100%)
- `test_invalid_pressure` - Pressure validation (900-1100 hPa)
- `test_negative_wind_speed` - Wind speed validation (0-200 mph)
- `test_multiple_invalid_fields` - Multiple validation failures
- `test_score_never_negative` - Score capped at 0.0
- `test_boundary_values` - Min/max boundary conditions

### test_weather_processing.py (6 tests)

**TestWeatherProcessing:**
- `test_api_data_transformation` - API response to database record
- `test_missing_weather_field` - Error handling for incomplete data
- `test_city_name_trimming` - City name normalization (documents expected behavior)
- `test_shared_timestamp` - Multiple cities with identical timestamp

**TestDatabaseSchema:**
- `test_required_fields_present` - All required fields exist
- `test_data_types` - Correct data types for each field

## Test Results
```
14 passed in 0.23s
```

**Success Rate:** 100%

## Fixtures (conftest.py)

### sample_weather_data
Sample API response from OpenWeatherMap

### sample_weather_record
Processed weather record ready for database

### invalid_weather_data
Edge case data with multiple validation failures

## What's Tested

✅ **Data Quality Validation:**
- Temperature range checking
- Humidity bounds (0-100%)
- Pressure validation
- Wind speed validation
- Quality score calculation (0.0-1.0)
- Multiple failure handling

✅ **Data Transformation:**
- API response parsing
- Field extraction and mapping
- Data type conversions
- Error handling for missing fields

✅ **Database Schema:**
- Required field presence
- Data type correctness
- Timestamp handling

## What's NOT Tested (Intentionally)

❌ **External Dependencies:**
- Live API calls to OpenWeatherMap
- Actual database connections
- AWS Lambda execution
- Network operations

**Why:** Unit tests focus on business logic isolation. Integration tests would require live services.

## Test Philosophy

**Unit Tests Focus:**
- Pure functions
- Business logic
- Data validation rules
- Edge cases and boundaries

**Fast Execution:**
- All tests run in <1 second
- No external dependencies
- Can run offline

**Maintainability:**
- Clear test names describe what's tested
- Fixtures provide reusable test data
- Tests document expected behavior

## Future Test Enhancements

**Nice to Have:**
- [ ] Integration tests with test database
- [ ] Mock API response tests
- [ ] Lambda handler integration tests
- [ ] Performance/load tests
- [ ] Property-based testing (hypothesis)
- [ ] Test data generation

## Continuous Integration

**Ready for CI/CD:**
```yaml
# Example GitHub Actions
- name: Run tests
  run: |
    pip install -r requirements.txt
    pytest -v --cov=src
```

## Coverage Notes

**Coverage Warning:** Expected and acceptable

Tests validate extracted logic functions, not the full `src/` scripts which require:
- Live AWS credentials
- Database connections
- API keys
- Environment variables

This is intentional - unit tests should be fast and isolated.

## Interview Talking Points

**"I implemented unit tests using pytest to validate data quality logic and transformation functions."**

**Key Points:**
- 14 tests, 100% passing
- Tests boundary conditions (min/max values)
- Tests edge cases (multiple failures, negative values)
- Fast execution (<1 second)
- No external dependencies required
- Demonstrates software engineering discipline
- Shows I think about data quality and edge cases

**Why It Matters:**
"Most data engineers don't write tests. Adding a test suite shows I approach data engineering with software engineering rigor - thinking about edge cases, documenting expected behavior, and ensuring code quality."

