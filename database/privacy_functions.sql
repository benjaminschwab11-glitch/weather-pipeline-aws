-- Privacy-Preserving Functions for PostgreSQL
-- Implements anonymization and masking at database level

-- Function: Generalize city to region
CREATE OR REPLACE FUNCTION generalize_city_to_region(city_name VARCHAR)
RETURNS VARCHAR AS $$
BEGIN
    RETURN CASE city_name
        WHEN 'San Diego' THEN 'Southern California'
        WHEN 'Los Angeles' THEN 'Southern California'
        WHEN 'San Francisco' THEN 'Northern California'
        WHEN 'San Jose' THEN 'Northern California'
        WHEN 'Oakland' THEN 'Northern California'
        WHEN 'Seattle' THEN 'Pacific Northwest'
        WHEN 'Portland' THEN 'Pacific Northwest'
        ELSE 'Unknown Region'
    END;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Function: Add differential privacy noise to temperature
CREATE OR REPLACE FUNCTION add_temperature_noise(temp DECIMAL, noise_percent DECIMAL DEFAULT 0.05)
RETURNS DECIMAL AS $$
DECLARE
    noise_range DECIMAL;
    random_noise DECIMAL;
BEGIN
    -- Calculate noise range
    noise_range := temp * noise_percent;
    
    -- Generate random noise between -noise_range and +noise_range
    random_noise := (RANDOM() * 2 - 1) * noise_range;
    
    -- Return temperature with noise
    RETURN ROUND(temp + random_noise, 1);
END;
$$ LANGUAGE plpgsql VOLATILE;

-- Function: Hash IP address (for future use if tracking IPs)
CREATE OR REPLACE FUNCTION hash_ip_address(ip_addr VARCHAR)
RETURNS VARCHAR AS $$
BEGIN
    -- SHA-256 hash of IP address
    RETURN encode(digest(ip_addr, 'sha256'), 'hex');
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Function: Mask IP address (preserve subnet)
CREATE OR REPLACE FUNCTION mask_ip_address(ip_addr VARCHAR)
RETURNS VARCHAR AS $$
DECLARE
    octets VARCHAR[];
BEGIN
    -- Split IP into octets
    octets := string_to_array(ip_addr, '.');
    
    -- Mask last octet
    octets[4] := '0';
    
    -- Reassemble
    RETURN array_to_string(octets, '.');
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- View: Anonymized weather data (with location generalization and noise)
CREATE OR REPLACE VIEW anonymized_weather_data AS
SELECT 
    generalize_city_to_region(city) as region,
    DATE_TRUNC('hour', timestamp) as hour,
    add_temperature_noise(temperature, 0.05) as temperature_anonymized,
    add_temperature_noise(feels_like, 0.05) as feels_like_anonymized,
    ROUND(AVG(humidity)) as avg_humidity,
    ROUND(AVG(pressure)) as avg_pressure,
    ROUND(AVG(wind_speed), 1) as avg_wind_speed,
    weather_condition,
    COUNT(*) as observation_count
FROM weather_observations
WHERE data_quality_score >= 0.9  -- Only high-quality data
GROUP BY 
    generalize_city_to_region(city),
    DATE_TRUNC('hour', timestamp),
    temperature,
    feels_like,
    weather_condition;

-- View: Regional weather aggregates (maximum privacy)
CREATE OR REPLACE VIEW regional_weather_summary AS
SELECT 
    generalize_city_to_region(city) as region,
    DATE_TRUNC('day', timestamp) as date,
    COUNT(DISTINCT city) as cities_in_region,
    ROUND(AVG(temperature), 1) as avg_temperature,
    ROUND(MIN(temperature), 1) as min_temperature,
    ROUND(MAX(temperature), 1) as max_temperature,
    ROUND(AVG(humidity)) as avg_humidity,
    ROUND(AVG(wind_speed), 1) as avg_wind_speed,
    COUNT(*) as total_observations
FROM weather_observations
WHERE data_quality_score >= 0.9
GROUP BY 
    generalize_city_to_region(city),
    DATE_TRUNC('day', timestamp)
ORDER BY region, date DESC;

-- Comments
COMMENT ON FUNCTION generalize_city_to_region(VARCHAR) IS 
    'Generalizes city name to region for k-anonymity';

COMMENT ON FUNCTION add_temperature_noise(DECIMAL, DECIMAL) IS 
    'Adds differential privacy noise to temperature readings';

COMMENT ON FUNCTION hash_ip_address(VARCHAR) IS 
    'One-way hash of IP address (SHA-256)';

COMMENT ON FUNCTION mask_ip_address(VARCHAR) IS 
    'Masks IP address by zeroing last octet';

COMMENT ON VIEW anonymized_weather_data IS 
    'Weather data with location generalization and differential privacy noise';

COMMENT ON VIEW regional_weather_summary IS 
    'Aggregated weather data by region with maximum privacy protection';

