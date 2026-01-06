-- Compliance Tables for GDPR/CCPA
-- Supports Data Subject Access Requests and Right to be Forgotten

-- User Consent Tracking Table
CREATE TABLE IF NOT EXISTS user_consent (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    consent_type VARCHAR(100) NOT NULL,
    consent_granted BOOLEAN NOT NULL,
    consent_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    consent_version VARCHAR(50),
    ip_address INET,
    user_agent TEXT,
    expiration_date TIMESTAMP WITH TIME ZONE,
    withdrawn_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for consent queries
CREATE INDEX idx_user_consent_user_id ON user_consent(user_id);
CREATE INDEX idx_user_consent_type ON user_consent(consent_type);
CREATE INDEX idx_user_consent_granted ON user_consent(consent_granted);
CREATE INDEX idx_user_consent_timestamp ON user_consent(consent_timestamp DESC);

-- Data Subject Access Request (DSAR) Table
CREATE TABLE IF NOT EXISTS data_subject_requests (
    id SERIAL PRIMARY KEY,
    request_id UUID DEFAULT gen_random_uuid() UNIQUE NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    request_type VARCHAR(50) NOT NULL, -- 'ACCESS', 'DELETION', 'RECTIFICATION', 'PORTABILITY'
    request_status VARCHAR(50) NOT NULL DEFAULT 'PENDING', -- 'PENDING', 'IN_PROGRESS', 'COMPLETED', 'REJECTED'
    request_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_timestamp TIMESTAMP WITH TIME ZONE,
    requester_email VARCHAR(255),
    requester_ip INET,
    verification_method VARCHAR(100),
    verification_status VARCHAR(50),
    data_exported_at TIMESTAMP WITH TIME ZONE,
    data_deleted_at TIMESTAMP WITH TIME ZONE,
    deletion_confirmation_code VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for DSAR queries
CREATE INDEX idx_dsar_request_id ON data_subject_requests(request_id);
CREATE INDEX idx_dsar_user_id ON data_subject_requests(user_id);
CREATE INDEX idx_dsar_type ON data_subject_requests(request_type);
CREATE INDEX idx_dsar_status ON data_subject_requests(request_status);
CREATE INDEX idx_dsar_timestamp ON data_subject_requests(request_timestamp DESC);

-- Data Deletion Log Table
CREATE TABLE IF NOT EXISTS data_deletion_log (
    id SERIAL PRIMARY KEY,
    deletion_id UUID DEFAULT gen_random_uuid() UNIQUE NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    request_id UUID REFERENCES data_subject_requests(request_id),
    table_name VARCHAR(100) NOT NULL,
    records_deleted INTEGER NOT NULL,
    deletion_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    deletion_method VARCHAR(50), -- 'HARD_DELETE', 'SOFT_DELETE', 'ANONYMIZE'
    backup_location VARCHAR(500),
    executed_by VARCHAR(100),
    verification_hash VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index for deletion log
CREATE INDEX idx_deletion_log_user_id ON data_deletion_log(user_id);
CREATE INDEX idx_deletion_log_request_id ON data_deletion_log(request_id);
CREATE INDEX idx_deletion_log_timestamp ON data_deletion_log(deletion_timestamp DESC);

-- View: Active Consents
CREATE OR REPLACE VIEW active_user_consents AS
SELECT 
    user_id,
    consent_type,
    consent_granted,
    consent_timestamp,
    consent_version,
    expiration_date,
    CASE 
        WHEN withdrawn_at IS NOT NULL THEN 'WITHDRAWN'
        WHEN expiration_date IS NOT NULL AND expiration_date < NOW() THEN 'EXPIRED'
        ELSE 'ACTIVE'
    END as consent_status
FROM user_consent
WHERE withdrawn_at IS NULL
  AND (expiration_date IS NULL OR expiration_date > NOW())
ORDER BY user_id, consent_timestamp DESC;

-- View: Pending DSAR Requests
CREATE OR REPLACE VIEW pending_dsar_requests AS
SELECT 
    request_id,
    user_id,
    request_type,
    request_status,
    request_timestamp,
    requester_email,
    EXTRACT(DAY FROM NOW() - request_timestamp) as days_pending,
    CASE 
        WHEN EXTRACT(DAY FROM NOW() - request_timestamp) > 30 THEN 'OVERDUE'
        WHEN EXTRACT(DAY FROM NOW() - request_timestamp) > 20 THEN 'WARNING'
        ELSE 'ON_TIME'
    END as sla_status
FROM data_subject_requests
WHERE request_status IN ('PENDING', 'IN_PROGRESS')
ORDER BY request_timestamp ASC;

-- Function: Record user consent
CREATE OR REPLACE FUNCTION record_user_consent(
    p_user_id VARCHAR,
    p_consent_type VARCHAR,
    p_granted BOOLEAN,
    p_version VARCHAR DEFAULT '1.0',
    p_ip_address INET DEFAULT NULL
)
RETURNS INTEGER AS $$
DECLARE
    v_consent_id INTEGER;
BEGIN
    INSERT INTO user_consent (
        user_id,
        consent_type,
        consent_granted,
        consent_version,
        ip_address
    ) VALUES (
        p_user_id,
        p_consent_type,
        p_granted,
        p_version,
        p_ip_address
    )
    RETURNING id INTO v_consent_id;
    
    -- Log to audit
    INSERT INTO audit_log (
        event_type,
        table_name,
        user_id,
        event_timestamp,
        details
    ) VALUES (
        'CONSENT_CHANGE',
        'user_consent',
        p_user_id,
        NOW(),
        jsonb_build_object(
            'consent_type', p_consent_type,
            'granted', p_granted,
            'consent_id', v_consent_id
        )
    );
    
    RETURN v_consent_id;
END;
$$ LANGUAGE plpgsql;

-- Function: Create DSAR request
CREATE OR REPLACE FUNCTION create_dsar_request(
    p_user_id VARCHAR,
    p_request_type VARCHAR,
    p_requester_email VARCHAR DEFAULT NULL
)
RETURNS UUID AS $$
DECLARE
    v_request_id UUID;
BEGIN
    INSERT INTO data_subject_requests (
        user_id,
        request_type,
        requester_email,
        request_status
    ) VALUES (
        p_user_id,
        p_request_type,
        p_requester_email,
        'PENDING'
    )
    RETURNING request_id INTO v_request_id;
    
    -- Log to audit
    INSERT INTO audit_log (
        event_type,
        table_name,
        user_id,
        event_timestamp,
        details
    ) VALUES (
        'DSAR_REQUEST',
        'data_subject_requests',
        p_user_id,
        NOW(),
        jsonb_build_object(
            'request_id', v_request_id,
            'request_type', p_request_type,
            'requester_email', p_requester_email
        )
    );
    
    RETURN v_request_id;
END;
$$ LANGUAGE plpgsql;

-- Comments
COMMENT ON TABLE user_consent IS 
    'Tracks user consent for data processing activities';

COMMENT ON TABLE data_subject_requests IS 
    'GDPR/CCPA data subject access requests and right to be forgotten';

COMMENT ON TABLE data_deletion_log IS 
    'Audit trail for all data deletion operations';

COMMENT ON VIEW active_user_consents IS 
    'Shows current active consent status per user';

COMMENT ON VIEW pending_dsar_requests IS 
    'Pending data subject requests with SLA tracking';

COMMENT ON FUNCTION record_user_consent IS 
    'Records user consent and logs to audit trail';

COMMENT ON FUNCTION create_dsar_request IS 
    'Creates a new data subject access request';

