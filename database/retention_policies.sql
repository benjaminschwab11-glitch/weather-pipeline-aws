-- Data Retention Policies
-- Automated deletion of data older than retention period

-- Retention policy for weather observations (365 days)
CREATE OR REPLACE FUNCTION cleanup_old_weather_data()
RETURNS TABLE(deleted_count INTEGER) AS $$
DECLARE
    v_deleted_count INTEGER;
    v_retention_days INTEGER := 365;
    v_cutoff_date TIMESTAMP;
BEGIN
    -- Calculate cutoff date
    v_cutoff_date := NOW() - INTERVAL '1 day' * v_retention_days;
    
    -- Delete old records
    DELETE FROM weather_observations
    WHERE timestamp < v_cutoff_date;
    
    GET DIAGNOSTICS v_deleted_count = ROW_COUNT;
    
    -- Log the deletion
    INSERT INTO audit_log (
        event_type,
        table_name,
        records_affected,
        event_timestamp,
        details
    ) VALUES (
        'DATA_RETENTION_CLEANUP',
        'weather_observations',
        v_deleted_count,
        NOW(),
        jsonb_build_object(
            'retention_days', v_retention_days,
            'cutoff_date', v_cutoff_date,
            'deleted_count', v_deleted_count
        )
    );
    
    RETURN QUERY SELECT v_deleted_count;
END;
$$ LANGUAGE plpgsql;

-- Retention policy for quality metrics (90 days)
CREATE OR REPLACE FUNCTION cleanup_old_quality_metrics()
RETURNS TABLE(deleted_count INTEGER) AS $$
DECLARE
    v_deleted_count INTEGER;
    v_retention_days INTEGER := 90;
    v_cutoff_date TIMESTAMP;
BEGIN
    -- Calculate cutoff date
    v_cutoff_date := NOW() - INTERVAL '1 day' * v_retention_days;
    
    -- Delete old records
    DELETE FROM quality_metrics
    WHERE collection_timestamp < v_cutoff_date;
    
    GET DIAGNOSTICS v_deleted_count = ROW_COUNT;
    
    -- Log the deletion
    INSERT INTO audit_log (
        event_type,
        table_name,
        records_affected,
        event_timestamp,
        details
    ) VALUES (
        'DATA_RETENTION_CLEANUP',
        'quality_metrics',
        v_deleted_count,
        NOW(),
        jsonb_build_object(
            'retention_days', v_retention_days,
            'cutoff_date', v_cutoff_date,
            'deleted_count', v_deleted_count
        )
    );
    
    RETURN QUERY SELECT v_deleted_count;
END;
$$ LANGUAGE plpgsql;

-- View to check retention compliance
CREATE OR REPLACE VIEW retention_compliance AS
SELECT 
    'weather_observations' as table_name,
    365 as retention_days,
    COUNT(*) as total_records,
    COUNT(*) FILTER (WHERE timestamp < NOW() - INTERVAL '365 days') as records_to_delete,
    MIN(timestamp) as oldest_record,
    MAX(timestamp) as newest_record,
    CASE 
        WHEN COUNT(*) FILTER (WHERE timestamp < NOW() - INTERVAL '365 days') > 0 
        THEN 'NON_COMPLIANT'
        ELSE 'COMPLIANT'
    END as compliance_status
FROM weather_observations
UNION ALL
SELECT 
    'quality_metrics' as table_name,
    90 as retention_days,
    COUNT(*) as total_records,
    COUNT(*) FILTER (WHERE collection_timestamp < NOW() - INTERVAL '90 days') as records_to_delete,
    MIN(collection_timestamp) as oldest_record,
    MAX(collection_timestamp) as newest_record,
    CASE 
        WHEN COUNT(*) FILTER (WHERE collection_timestamp < NOW() - INTERVAL '90 days') > 0 
        THEN 'NON_COMPLIANT'
        ELSE 'COMPLIANT'
    END as compliance_status
FROM quality_metrics;

-- Comments
COMMENT ON FUNCTION cleanup_old_weather_data() IS 
    'Deletes weather observations older than 365 days per retention policy';
    
COMMENT ON FUNCTION cleanup_old_quality_metrics() IS 
    'Deletes quality metrics older than 90 days per retention policy';

COMMENT ON VIEW retention_compliance IS 
    'Shows retention policy compliance status for all tables';

