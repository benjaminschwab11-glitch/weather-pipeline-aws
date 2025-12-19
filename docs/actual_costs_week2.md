# Actual Costs - Week 2 Analysis

**Reporting Period:** December 12-17, 2024 (6 days)  
**Pipeline Status:** Fully automated since December 16, 9:30 PM

## Lambda Execution Costs

**Executions (Dec 16-17):**
- Time running: ~24 hours
- Expected executions: 96
- Actual executions: [Fill from CloudWatch]
- Success rate: [Fill from CloudWatch]

**Compute Costs:**
- Executions: ~96
- Average duration: ~10 seconds
- Memory: 128 MB
- GB-seconds: 96 × 10 × (128/1024) = 120 GB-seconds
- Cost: 120 × $0.0000166667 = **$0.002**
- Free tier: 400,000 GB-seconds/month
- **Actual cost: $0.00** (within free tier)

## RDS Database Costs

**Instance:**
- Type: db.t3.micro
- Hours: 144 hours (6 days)
- Rate: ~$0.017/hour
- Cost: 144 × $0.017 = **$2.45**
- Free tier: 750 hours/month
- **Actual cost: $0.00** (within free tier for first 12 months)

## EventBridge Scheduler Costs

**Invocations:**
- Count: ~96 in 24 hours
- Rate: $1.00 per 1M invocations
- Cost: 96 × ($1.00 / 1,000,000) = **$0.000096**
- Free tier: 14M invocations/month
- **Actual cost: $0.00** (within free tier)

## Data Transfer Costs

**Outbound:**
- API calls: ~96 × 5 cities × ~2 KB = ~1 MB
- CloudWatch logs: ~96 × ~5 KB = ~0.5 MB
- Total: ~1.5 MB
- Free tier: 100 GB/month
- **Actual cost: $0.00** (negligible)

## CloudWatch Logs Costs

**Storage:**
- Log data: ~96 executions × ~5 KB = ~0.5 MB
- Rate: $0.50/GB ingested
- Cost: 0.0005 GB × $0.50 = **$0.00025**
- Free tier: 5 GB ingested/month
- **Actual cost: $0.00** (within free tier)

## Total Week 2 Costs

| Service | Estimated | Actual | Free Tier Applied |
|---------|-----------|--------|-------------------|
| Lambda | $0.002 | $0.00 | ✅ Yes |
| RDS | $2.45 | $0.00 | ✅ Yes |
| EventBridge | $0.0001 | $0.00 | ✅ Yes |
| CloudWatch | $0.0003 | $0.00 | ✅ Yes |
| **TOTAL** | **$2.45** | **$0.00** | ✅ Free tier covers all |

## Projected Monthly Costs (After Free Tier)

**When free tier expires (after 12 months):**
- RDS db.t3.micro: ~$15/month
- Lambda: ~$0.20/month
- EventBridge: ~$0.003/month
- CloudWatch: ~$0.01/month
- **Total: ~$15.21/month**

## Cost Optimization Opportunities

1. **RDS:** Could migrate to Aurora Serverless v2 for ~$8/month
2. **Lambda:** Already optimized (128 MB memory sufficient)
3. **CloudWatch:** Could reduce log retention to 7 days
4. **EventBridge:** Already minimal cost

## Conclusion

**Current Phase (with free tier):** $0.00/month ✅  
**Production Phase (post free tier):** ~$15/month  
**Cost per weather observation:** ~$0.005  
**Cost per city tracked per month:** ~$3.04

**Value:** Production-grade automated data pipeline for portfolio demonstration at zero current cost.

