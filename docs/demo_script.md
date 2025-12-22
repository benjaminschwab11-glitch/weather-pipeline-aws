# Project Demo Script

## 2-Minute Version (Interview Opening)

**"I built an end-to-end real-time data pipeline that demonstrates modern cloud-native data engineering."**

### Live Demo Flow:

**1. Show Dashboard (30 seconds)**
- "This is my live dashboard - it's publicly accessible at this URL"
- "Shows current weather for 5 West Coast cities updated every 15 minutes"
- "Temperature trends, humidity distributions, all interactive"

**2. Show Architecture (45 seconds)**
- "The pipeline runs entirely on AWS, fully automated"
- "EventBridge triggers Lambda every 15 minutes"
- "Lambda calls the OpenWeatherMap API, processes 5 cities"
- "Stores in RDS PostgreSQL with data quality scoring"
- "CloudWatch monitors everything"
- "Streamlit dashboard queries RDS and displays live"

**3. Show Code (30 seconds)**
- "Here's the Lambda function - production-grade error handling"
- "Notice the shared timestamp approach - prevents duplicate conflicts"
- "Data quality validation built in from day one"

**4. Key Technical Decisions (15 seconds)**
- "Chose Lambda over EC2 for zero server management"
- "PostgreSQL over DynamoDB to leverage my SQL expertise"
- "Fixed a timestamp bug that was costing 80% of my data"

---

## 5-Minute Technical Deep Dive

**If they ask for details:**

### Problem I Solved:
"I wanted to prove I could build modern cloud-native systems, not just maintain legacy ETL. I have 25 years in traditional data warehousing - Informatica, Oracle, on-prem. I needed to show I could architect serverless, real-time, cloud platforms."

### Technical Highlights:

**1. Data Quality Built In**
- "Every record gets a quality score 0.0 to 1.0"
- "Validates temperature, humidity, pressure ranges"
- "Currently maintaining 100% quality across 2,000+ observations"

**2. Timestamp Conflict Resolution**
- "Initially only storing 1 city per execution instead of 5"
- "Root cause: microsecond timestamp differences triggering unique constraint"
- "Solution: Single timestamp per collection run - all 5 cities share it"
- "Went from 96 records/day to 480 - 5x efficiency gain"

**3. Cost Optimization**
- "Entire pipeline costs $0 on free tier"
- "Post free tier: ~$15/month"
- "2,880 Lambda executions/month"
- "Serverless = pay per use, scales automatically"

**4. Production Practices**
- "CloudWatch logging on every execution"
- "Custom metrics published (records collected, execution time)"
- "Error handling with exponential backoff"
- "Infrastructure as code ready (can add Terraform)"

### What I Learned:

**Technical:**
- "Lambda binary dependencies need platform-specific builds"
- "execute_batch cursor.rowcount is unreliable - use len(data)"
- "Security groups work differently for Lambda than local dev"

**Soft Skills:**
- "Late-night debugging isn't always best - I rolled back and fixed fresh"
- "Built in 12 days through consistent daily execution"
- "Documentation as you go beats trying to remember later"

---

## Common Interview Questions

**Q: Why did you build this?**
A: "To prove I can design modern cloud-native data platforms, not just maintain legacy systems. My background is traditional ETL - this shows I've modernized."

**Q: What would you do differently?**
A: "Add unit tests from day one. Implement Terraform for IaC. Consider Aurora Serverless for better cost scaling. Add data quality alerting via SNS."

**Q: How would you scale this?**
A: "Add more cities - Lambda scales automatically. Partition RDS tables by date for query performance. Add caching layer (ElastiCache) for dashboard. Implement data quality anomaly detection with Lambda."

**Q: What was the hardest part?**
A: "The timestamp conflict bug. Took me a while to diagnose why only 1 record was inserting. The fix was elegant - single shared timestamp - but finding it required careful log analysis and database investigation."

**Q: How much does this cost to run?**
A: "Currently $0 on free tier. Post free tier about $15/month. Could optimize to ~$8/month with Aurora Serverless v2. Lambda is only $0.20/month - serverless wins on cost."

---

## Key Talking Points

✅ **Real production pipeline** - not a tutorial, not Kaggle  
✅ **Live 24/7** - collecting data while we talk  
✅ **Public dashboard** - you can access it right now  
✅ **Modern stack** - Lambda, EventBridge, RDS, Streamlit  
✅ **DBA thinking** - data quality, schema design, indexing  
✅ **SRE principles** - monitoring, error budgets, observability  
✅ **12 days start to finish** - rapid execution, consistent progress  

---

## Links Ready to Share

**Dashboard:** https://weather-pipeline-aws-f2ov36k74bnjfmhmcvbikw.streamlit.app  
**GitHub:** https://github.com/benjaminschwab11-glitch/weather-pipeline-aws  
**LinkedIn:** www.linkedin.com/in/bschwab03

