# Week 2 Retrospective

**Dates:** December 12-17, 2024  
**Goal:** Migrate from local execution to AWS Lambda automation

## ✅ What We Accomplished

### Day 7 (Dec 12)
- Lambda function code prepared
- Lambda-compatible deployment package created
- Local testing successful

### Day 8 (Dec 15)
- Lambda function deployed to AWS
- Resolved psycopg2 binary compatibility issue
- Fixed RDS security group for Lambda access
- Manual invocation successful
- Data flowing from Lambda to RDS

### Day 9 (Dec 16)
- EventBridge Scheduler configured
- Automated execution every 15 minutes
- First scheduled execution verified
- Local scheduler retired
- Full automation achieved

### Day 10 (Dec 17)
- 24-hour performance review
- Cost analysis completed
- Pipeline performance validated

## 📊 Week 2 Metrics

**Technical Accomplishments:**
- Lambda executions: ~96 in 24 hours
- Success rate: [Fill]%
- Records collected automatically: [Fill]
- Uptime: 24/7 since Dec 16, 9:30 PM
- Manual intervention required: 0

**Cost Performance:**
- Estimated: ~$2.45
- Actual: $0.00 (free tier coverage)
- Efficiency: 100% free tier utilization

## 💪 What Went Well

1. **Lambda deployment smoother than expected** - psycopg2 issue resolved quickly
2. **EventBridge Scheduler intuitive** - easier than anticipated
3. **Troubleshooting skills applied** - Security group, binary dependencies
4. **Documentation discipline maintained** - Clear records of all decisions
5. **Automation works flawlessly** - Zero manual intervention in 24 hours

## 🎯 Challenges Overcome

### Challenge 1: psycopg2 Binary Compatibility
**Issue:** psycopg2-binary compiled for Mac won't work in Lambda (Linux)  
**Solution:** Used pre-compiled Lambda-compatible psycopg2 from GitHub  
**Learning:** Always check binary dependencies for platform compatibility

### Challenge 2: Lambda-RDS Connectivity
**Issue:** Initial Lambda test timed out connecting to RDS  
**Root Cause:** Security group only allowed personal IP, not Lambda  
**Solution:** Updated RDS security group to allow Lambda access (0.0.0.0/0)  
**Learning:** Lambda runs from AWS IP ranges, not your local IP

### Challenge 3: EventBridge Interface Confusion
**Issue:** Started in "Rules" instead of "Scheduler"  
**Solution:** Found correct EventBridge Scheduler section  
**Learning:** AWS has multiple ways to schedule - Scheduler is simpler for this use case

## 🧠 Key Technical Learnings

1. **Lambda Layers aren't always accessible** - Public layers may have permission issues
2. **Security groups are critical** - Lambda networking differs from local development
3. **CloudWatch is essential** - Only way to debug Lambda in production
4. **Free tier is generous** - $0 cost for real production workload
5. **Serverless means truly autonomous** - No server management, just works

## 📝 What Could Be Better

1. **Testing:** Still no automated tests (unit or integration)
2. **Monitoring:** Could add CloudWatch alarms for failures
3. **Documentation:** Could add architecture diagram
4. **Error handling:** Lambda retries not explicitly tested

## 🎯 Week 3 Priorities


### Must Have (Core Dashboard)
- [ ] Create Streamlit dashboard locally
- [ ] Display current weather conditions
- [ ] Show temperature trends over time
- [ ] Deploy dashboard to Streamlit Cloud

### Nice to Have (Enhanced Features)
- [ ] Add data quality dashboard
- [ ] CloudWatch alarm for Lambda failures
- [ ] SNS email notifications
- [ ] Pipeline health metrics

### Can Wait (Future Enhancements)
- [ ] Add more cities
- [ ] Multiple data sources (air quality, etc.)
- [ ] Predictive models
- [ ] Terraform IaC

## 💭 Personal Reflections

**What surprised me:** 
How simple it was to add the python function as a lambda function and then get it scheduled using EventBridge.

**What I'm proud of:** 
I'm proud that I'm learning by building.

**What I learned about cloud engineering:** 
A simple data app like this can be very quick and easy to build.

**How I feel about Week 3 (visualization):** 
I'm excited to see what else I will learn to build with this project and how I can take that into other things I may want to play around with and learn.

## 🎯 Success Criteria for Week 3

By December 24, 2024:
- [ ] Working Streamlit dashboard
- [ ] Deployed to public URL
- [ ] Shows last 7 days of data
- [ ] Updated README with dashboard link
- [ ] Demo-ready for interviews

---

**Week 2: ✅ COMPLETE - AWS Migration Successful**  
**Pipeline Status: Fully Operational and Autonomous**  
**Next: Week 3 - Data Visualization**

