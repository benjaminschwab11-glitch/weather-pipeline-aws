# Monitoring & Alerting Configuration

**Region:** us-west-2 (Oregon)  
**Deployed:** December 24, 2024

## CloudWatch Dashboard

**Dashboard Name:** weather-pipeline-monitoring  
**Auto-refresh:** 1 minute  
**Region:** us-west-2

### Dashboard Widgets

**1. Lambda Invocations & Errors**
- **Type:** Line graph
- **Metrics:** Invocations, Errors, Throttles
- **Statistic:** Sum
- **Period:** 15 minutes
- **Expected:** 4 invocations/hour, 0 errors, 0 throttles

**2. Execution Duration**
- **Type:** Line graph
- **Metric:** Duration (Average)
- **Period:** 15 minutes
- **Expected:** 8-12 seconds average
- **Alert threshold:** >15 seconds

**3. Pipeline Custom Metrics**
- **Type:** Line graph
- **Metrics:** RecordsCollected, RecordsStored, ExecutionTime
- **Period:** 15 minutes
- **Expected:** 
  - RecordsCollected: 5 per execution
  - RecordsStored: 5 per execution
  - ExecutionTime: 3,000-5,000 ms

**4. Errors (Last Hour)**
- **Type:** Number widget
- **Metric:** Errors (Sum)
- **Period:** 1 hour
- **Expected:** 0

**5. Success Rate (Last Hour)**
- **Type:** Number widget
- **Formula:** `100 - (Errors/Invocations * 100)`
- **Period:** 1 hour
- **Expected:** 100%

## SNS Alerts

**Topic Name:** weather-pipeline-alerts  
**Topic ARN:** arn:aws:sns:us-west-2:[account]:weather-pipeline-alerts  
**Display Name:** Weather Pipeline

**Note:** Email subscription disabled during development. Alarms trigger and log to CloudWatch. For production deployment, would enable email or SMS notifications.

## CloudWatch Alarms

### 1. Lambda Errors Alert

**Alarm Name:** weather-pipeline-errors  
**Metric:** AWS/Lambda Errors  
**Condition:** Errors ≥ 2 in 5 minutes  
**Statistic:** Sum  
**Period:** 5 minutes  
**Action:** Configured to send to SNS topic  
**Purpose:** Immediate notification of pipeline failures  
**Status:** Active ✅

---

### 2. Slow Execution Alert

**Alarm Name:** weather-pipeline-slow-execution  
**Metric:** AWS/Lambda Duration  
**Condition:** Duration > 15,000 ms (15 seconds)  
**Statistic:** Average  
**Period:** 5 minutes  
**Action:** Configured to send to SNS topic  
**Purpose:** Performance degradation warning  
**Status:** Active ✅

---

### 3. Pipeline Stopped Alert

**Alarm Name:** weather-pipeline-not-running  
**Metric:** AWS/Lambda Invocations  
**Condition:** Invocations < 3 in 1 hour  
**Statistic:** Sum  
**Period:** 1 hour  
**Treat missing data as:** Breaching  
**Action:** Configured to send to SNS topic  
**Purpose:** Detect if EventBridge schedule fails  
**Status:** Active ✅

## Monitoring Approach

**Real-time Monitoring:**
- CloudWatch Dashboard provides visual monitoring
- Auto-refresh every 1 minute
- All key metrics visible at a glance

**Alarm-based Monitoring:**
- CloudWatch Alarms evaluate metrics automatically
- Alarm states visible in CloudWatch console
- Can be extended to email/SMS/Slack notifications

**Manual Monitoring:**
- Check dashboard daily for trends
- Review alarm states in CloudWatch → Alarms
- Investigate any "In alarm" states immediately

## Alert Response Procedures

### 🚨 Lambda Error Alarm (In Alarm State)

**Step 1: Check CloudWatch Logs**
1. Lambda → weather-pipeline → Monitor → View CloudWatch logs
2. Click most recent log stream
3. Look for ERROR messages or exceptions

**Step 2: Common Causes**
- RDS security group blocking Lambda
- API key expired or rate limited
- Database connection timeout
- Recent code deployment issue

**Step 3: Quick Diagnostics**
- Verify RDS security group allows 0.0.0.0/0 on port 5432
- Check Lambda environment variables
- Manually invoke Lambda with test event
- Check RDS database status

---

### ⏱️ Slow Execution Alarm (In Alarm State)

**Step 1: Check Duration Trend**
- CloudWatch Dashboard → Duration graph
- Gradual increase vs. sudden spike?

**Step 2: Investigate**
- Check RDS CPU/memory metrics
- Review logs for slow API calls
- Check network latency

**Step 3: Solutions**
- Increase Lambda memory (128 MB → 256 MB)
- Optimize database queries
- Check for API throttling

---

### 🛑 Pipeline Stopped Alarm (In Alarm State)

**Step 1: Check EventBridge**
- EventBridge → Scheduler → Schedules
- Verify: weather-pipeline-schedule = Enabled

**Step 2: Check Lambda**
- Verify function exists
- Check IAM execution role

**Step 3: Manual Test**
- Lambda → Test
- If works: EventBridge issue
- If fails: Lambda issue

## Metrics Baseline (Normal Operation)

### Expected Values

**Invocations:**
- Per 15 minutes: 1
- Per hour: 4
- Per day: 96
- Per month: ~2,880

**Duration:**
- Average: 10 seconds
- Expected range: 8-12 seconds
- Alert threshold: >15 seconds

**Errors:**
- Expected: 0
- Acceptable: <1%

**Custom Metrics:**
- RecordsCollected: 5 per execution
- RecordsStored: 5 per execution
- ExecutionTime: 3,000-5,000 ms

**Success Rate:**
- Target: 100%
- Acceptable: >99%

### Red Flags 🚩

**RecordsStored < RecordsCollected**
- Database insertion failures
- Check RDS connectivity

**Duration increasing over time**
- Performance degradation
- Check RDS metrics

**Errors > 0**
- Pipeline failure
- Check CloudWatch logs

**Invocations < 4/hour**
- Schedule issue
- Check EventBridge

## Cost Analysis

**CloudWatch Alarms:**
- 3 alarms × $0.10/alarm/month = **$0.30/month**

**CloudWatch Dashboard:**
- First 3 dashboards = **Free**

**SNS Topic:**
- Topic creation = **Free**
- No active subscriptions = **$0.00**

**CloudWatch Logs:**
- 5 GB ingestion/month free tier
- Current usage: ~500 MB/month = **Free**

**Custom Metrics:**
- First 10,000 metrics free
- Current: 3 custom metrics = **Free**

**Total Monthly Cost: $0.30**

## Maintenance

**Daily:**
- Quick dashboard check for anomalies
- Verify alarms in OK state

**Weekly:**
- Review dashboard trends
- Check for any performance degradation

**Monthly:**
- Review costs in AWS Cost Explorer
- Verify all alarms still relevant

## Production Readiness

**Current State:**
- ✅ CloudWatch Dashboard operational
- ✅ 3 CloudWatch Alarms configured
- ✅ SNS topic configured (ready for subscriptions)
- ✅ Custom metrics publishing
- ✅ Response procedures documented

**For Production Deployment:**
- Add email/SMS/Slack notifications to SNS topic
- Set up on-call rotation
- Document escalation procedures
- Add more granular alarms if needed

