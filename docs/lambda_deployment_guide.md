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

