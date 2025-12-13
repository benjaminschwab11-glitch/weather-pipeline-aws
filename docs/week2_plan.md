# Week 2 Plan: AWS Lambda Migration

**Dates:** December 12-18, 2024  
**Goal:** Move from local scheduling to serverless cloud execution

## 🎯 End State

By December 18, you will have:
- Lambda function running in AWS
- EventBridge trigger (every 15 minutes)
- CloudWatch logs and metrics
- Local pipeline shut down (no longer needed)
- Data flowing without your laptop

## 📅 Day-by-Day Breakdown

### Day 7 (Dec 12) - Lambda Function Preparation
**Time:** 1.5-2 hours

**Tasks:**
- Create Lambda-compatible version of pipeline
- Package dependencies (requests, psycopg2)
- Test locally with Lambda handler pattern
- Create deployment package (ZIP file)

**Deliverable:** `lambda_function.zip` ready to upload

---

### Day 8 (Dec 13) - Initial Lambda Deployment
**Time:** 1.5-2 hours

**Tasks:**
- Create Lambda function in AWS Console
- Upload deployment package
- Configure environment variables
- Set timeout and memory
- Test with manual invocation

**Deliverable:** Lambda function executing successfully

---

### Day 9 (Dec 14) - EventBridge Integration
**Time:** 1 hour

**Tasks:**
- Create EventBridge rule (15-minute schedule)
- Connect rule to Lambda function
- Test automated triggers
- Verify RDS connectivity from Lambda

**Deliverable:** Automated execution working

---

### Day 10 (Dec 15) - CloudWatch Monitoring
**Time:** 1.5 hours

**Tasks:**
- Review CloudWatch Logs
- Create custom metrics
- Build CloudWatch dashboard
- Set up basic alarms

**Deliverable:** Monitoring operational

---

### Day 11 (Dec 16) - Testing & Validation
**Time:** 1 hour

**Tasks:**
- Let Lambda run for 24 hours
- Verify data quality
- Check for errors
- Compare local vs Lambda performance

**Deliverable:** Confidence in serverless operation

---

### Day 12 (Dec 17) - Documentation & Cleanup
**Time:** 1 hour

**Tasks:**
- Update README with Lambda architecture
- Document deployment process
- Create troubleshooting guide
- Shut down local scheduler

**Deliverable:** Complete Week 2 documentation

---

### Day 13 (Dec 18) - Week 2 Checkpoint
**Time:** 30 minutes

**Tasks:**
- Week 2 retrospective
- Assess data collection
- Plan Week 3 (visualization)

## 🚨 Potential Blockers

1. **Lambda VPC configuration** - If RDS is in VPC, Lambda needs VPC access
2. **Python dependencies size** - Lambda has 250MB limit (psycopg2 is large)
3. **Cold starts** - First invocation may timeout
4. **IAM permissions** - Lambda needs proper role for RDS access

## 💡 Success Criteria

- [ ] Lambda executes without errors
- [ ] Data flowing to RDS from Lambda
- [ ] CloudWatch logs show successful runs
- [ ] No local pipeline needed
- [ ] Cost remains under $1/month

## 📚 Resources Needed

- AWS Lambda documentation
- psycopg2 Lambda layer (pre-compiled)
- EventBridge cron expressions
- CloudWatch dashboards guide

---

**Ready to start Week 2 tomorrow.**

