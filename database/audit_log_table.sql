-- Audit Log Table
-- Tracks all data access, modifications, and deletions for compliance

CREATE TABLE IF NOT EXISTS audit_log (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(100) NOT NULL,
    table_name VARCHAR(100),
    record_id INTEGER,
    records_affected INTEGER,
    user_id VARCHAR(100),
    action VARCHAR(50),
    event_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ip_address INET,
    details JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for audit queries
CREATE INDEX idx_audit_event_type ON audit_log(event_type);
CREATE INDEX idx_audit_table_name ON audit_log(table_name);
CREATE INDEX idx_audit_timestamp ON audit_log(event_timestamp DESC);
CREATE INDEX idx_audit_user_id ON audit_log(user_id);

-- View for recent audit events
CREATE OR REPLACE VIEW recent_audit_events AS
SELECT 
    id,
    event_type,
    table_name,
    records_affected,
    user_id,
    event_timestamp,
    details->>'description' as description
FROM audit_log
ORDER BY event_timestamp DESC
LIMIT 100;

COMMENT ON TABLE audit_log IS 
    'Audit trail for all data access and modifications';

COMMENT ON COLUMN audit_log.event_type IS 
    'Type of event: DATA_ACCESS, DATA_MODIFICATION, DATA_DELETION, DATA_RETENTION_CLEANUP, etc.';

COMMENT ON COLUMN audit_log.details IS 
    'JSON details about the event (flexible schema)';

