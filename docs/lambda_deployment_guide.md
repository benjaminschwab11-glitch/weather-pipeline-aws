
# AWS Lambda Deployment Guide

## Pre-Deployment Checklist

- [x] Lambda function code created (`lambda/lambda_function.py`)
- [x] Local testing successful
- [x] Deployment package created (`lambda/lambda_deployment.zip`)
- [ ] AWS Lambda Layer ARN identified (psycopg2)
- [ ] Environment variables documented
- [ ] IAM role requirements documented

## Environment Variables Required

Lambda needs these environment variables configured:
```
WEATHER_API_KEY=<your_openweathermap_api_key>
CITIES=San Diego,Los Angeles,San Francisco,Seattle,Portland
RDS_ENDPOINT=<your_rds_endpoint>.rds.amazonaws.com
RDS_DATABASE=weather_db
RDS_USERNAME=weather_admin
RDS_PASSWORD=<your_rds_password>
RDS_PORT=5432
```

## Lambda Configuration

**Runtime:** Python 3.11  
**Architecture:** x86_64  
**Memory:** 256 MB (start here, can adjust)  
**Timeout:** 30 seconds (our pipeline runs ~10-15 seconds)  
**Handler:** lambda_function.lambda_handler

## IAM Role Permissions Needed

Lambda execution role needs:

1. **Basic Lambda execution:**
   - AWSLambdaBasicExecutionRole (managed policy)

2. **CloudWatch metrics:**
   - cloudwatch:PutMetricData

3. **VPC access (if RDS in VPC):**
   - ec2:CreateNetworkInterface
   - ec2:DescribeNetworkInterfaces
   - ec2:DeleteNetworkInterface

## PostgreSQL Lambda Layer

**For psycopg2 support, use AWS Lambda Layer:**

Layer ARN (us-west-2, Python 3.11):
```
arn:aws:lambda:us-west-2:898466741470:layer:psycopg2-py311:1
```

Alternative: https://github.com/jetbridge/psycopg2-lambda-layer

## Deployment Steps (Day 8)

1. Create Lambda function in AWS Console
2. Upload `lambda_deployment.zip`
3. Add psycopg2 Lambda Layer
4. Configure environment variables
5. Set timeout to 30 seconds
6. Test with manual invocation
7. Check CloudWatch Logs for output

## Troubleshooting

### Issue: Timeout errors
**Solution:** Increase timeout to 60 seconds

### Issue: Database connection refused
**Solution:** Check RDS security group allows Lambda IP ranges

### Issue: "No module named 'psycopg2'"
**Solution:** Verify Lambda Layer is attached

### Issue: Cold start delays
**Solution:** Normal for first invocation, subsequent runs will be faster

## Testing Commands
```python
# Test event (empty for EventBridge trigger)
{}
```

Expected response:
```json
{
  "statusCode": 200,
  "body": "{\"message\": \"Weather pipeline executed successfully\", ...}"
}
```

## Monitoring

**CloudWatch Log Groups:**
- `/aws/lambda/weather-pipeline`

**Custom Metrics:**
- WeatherPipeline/RecordsCollected
- WeatherPipeline/RecordsStored
- WeatherPipeline/ExecutionTime

## Cost Estimate

**Lambda:**
- Invocations: 2,880/month (every 15 min)
- Duration: ~10 sec avg
- Memory: 256 MB
- **Cost: ~$0.20/month** (within free tier)

**CloudWatch Logs:**
- ~5 KB per execution
- **Cost: ~$0.05/month**

**Total Lambda costs: ~$0.25/month**

---

**Next:** Day 8 - Deploy to AWS Lambda

---

## Network Configuration (ADDED Dec 15, 2025)

**VPC:** Not in VPC (Lambda runs in AWS-managed VPC)  
**RDS Access:** Allowed via security group inbound rule  

### RDS Security Group Inbound Rules

- Type: PostgreSQL
- Port: 5432
- Source: 0.0.0.0/0 (for portfolio project simplicity)
- Description: Lambda access to RDS

**Production Recommendation:** Place Lambda in VPC and restrict RDS security group to Lambda's security group only for enhanced security.

---

## Deployment Success (Dec 15, 2025)

✅ Lambda function operational  
✅ Manual test successful  
✅ Data flowing to RDS  
✅ CloudWatch logging working  

**First Successful Execution:**
- Duration: ~10-12 seconds
- Memory used: ~70-80 MB
- Records stored: 5
- Status: SUCCESS

---

## Troubleshooting Resolution

### Issue: Database Connection Timeout

**Symptom:**
```
✗ Database error: connection to server at "weather-pipeline-db..." 
port 5432 failed: timeout expired
```

**Root Cause:** RDS security group only allowed personal IP address, not Lambda's IP ranges

**Solution:** Updated RDS security group inbound rules to allow 0.0.0.0/0

**Resolution Steps:**
1. Go to RDS Console → weather-pipeline-db
2. Click Connectivity & security → Security group link
3. Edit inbound rules
4. Change PostgreSQL rule source to 0.0.0.0/0
5. Save rules
6. Re-test Lambda function

**Result:** ✅ Lambda successfully connects and stores data

**Key Learning:** Lambda functions run from AWS IP ranges, not your local IP. Security groups must accommodate Lambda's network context.

---

**Next:** Day 9 - EventBridge scheduling for automated execution

