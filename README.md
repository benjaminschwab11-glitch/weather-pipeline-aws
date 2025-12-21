# Real-Time Weather Data Pipeline

A production-quality data engineering pipeline demonstrating modern cloud-native practices: real-time API ingestion, data quality validation, cloud database storage, and automated scheduling.

## 🎯 Project Overview

**🌐 Live Dashboard:** [View Dashboard](https://weather-pipeline-aws-f2ov36k74bnjfmhmcvbikw.streamlit.app)  
**📂 GitHub Repository:** [Source Code](https://github.com/benjaminschwab11-glitch/weather-pipeline-aws)  
**Live Status:** ✅ Collecting data every 15 minutes, fully automated  
**Dataset:** 2,000+ weather observations (and growing)  
**Deployed:** December 20, 2024
```

** https://weather-pipeline-aws-f2ov36k74bnjfmhmcvbikw.streamlit.app **

---

**What's your Streamlit dashboard URL?** (So I can give you the exact line to paste)

It should look like:
```
https://benjaminschwab11-glitch-weather-pipeline-aws-dashboard-xxxxx.streamlit.app
## 🏗️ Architecture
```
OpenWeatherMap API → Python ETL → PostgreSQL (AWS RDS) → Dashboard (Coming)
         ↓              ↓              ↓
    Real-time      Validation    Cloud Storage
     Data          & Logging      & Indexing
```

### Current Components (Days 1-6)

- **Data Source:** OpenWeatherMap API (5 cities, 15-minute intervals)
- **Processing:** Python 3.x with data quality validation
- **Storage:** AWS RDS PostgreSQL 15 (db.t4g.micro)
- **Logging:** Structured logging with daily rotation
- **Scheduling:** Local scheduler (migrating to AWS Lambda)

### Coming Soon (Week 2-3)

- AWS Lambda deployment (serverless)
- EventBridge scheduling
- CloudWatch monitoring & alerts
- Streamlit dashboard

## 💡 Why This Project Matters

This project demonstrates the **modernization journey** from traditional data warehousing to cloud-native data engineering:

**Traditional Stack (My 25-year background):**
- Batch ETL (Informatica PowerCenter)
- On-prem Oracle databases
- Scheduled jobs (Control-M, cron)
- Manual server management

**Modern Cloud-Native Stack (This Project):**
- Real-time event-driven processing
- Serverless compute (AWS Lambda)
- Managed cloud databases (RDS)
- Infrastructure as Code
- Built-in monitoring & observability

## 🛠️ Technical Stack

**Languages & Core:**
- Python 3.11
- SQL (PostgreSQL)

**AWS Services:**
- RDS (PostgreSQL 15)
- Lambda (planned)
- EventBridge (planned)
- CloudWatch (planned)

**Libraries:**
- `requests` - API integration
- `psycopg2` - PostgreSQL driver
- `python-dotenv` - Environment management
- `schedule` - Local scheduling

## 📊 Current Metrics

*(As of December 11, 2024)*

- **Total Observations:** 100+
- **Cities Tracked:** 5 (San Diego, LA, SF, Seattle, Portland)
- **Data Quality:** 99%+ excellent scores
- **Collection Frequency:** Every 15 minutes
- **Database Size:** ~50 KB (and growing)

## 🚀 Setup & Installation

### Prerequisites

- Python 3.8+
- AWS Account (free tier)
- OpenWeatherMap API key

### Local Setup
```bash
# Clone repository
git clone https://github.com/yourusername/weather-pipeline-aws.git
cd weather-pipeline-aws

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your API keys and RDS credentials
```

### Run Pipeline
```bash
# Single execution
python src/weather_pipeline_scheduled.py

# Scheduled execution (every 15 minutes)
./start_pipeline.sh
```

## 📁 Project Structure
```
weather-pipeline-aws/
├── src/
│   ├── api_test.py                    # API connection testing
│   ├── db_test.py                     # Database connection testing
│   ├── weather_pipeline.py            # Core pipeline (Day 4)
│   ├── weather_pipeline_scheduled.py  # Production version with logging
│   ├── run_scheduled.py               # Local scheduler
│   ├── logger_config.py               # Logging configuration
│   ├── query_data.py                  # Data inspection utility
│   └── check_stats.py                 # Pipeline statistics
├── database/
│   └── schema.sql                     # PostgreSQL schema
├── docs/
│   └── progress.md                    # Daily progress log
├── logs/                              # Daily log files (git ignored)
├── .env                               # Secrets (git ignored)
├── requirements.txt                   # Python dependencies
└── README.md                          # This file
```

## 🎓 Key Learnings

### Data Quality
- Implemented validation scoring (0.0-1.0) based on range checks
- Tracks quality metrics per observation
- Logs quality issues for investigation

### Database Design
- Optimized indexes for time-series queries
- Unique constraints prevent duplicates
- Partition-ready schema for scaling

### Error Handling
- Comprehensive try/except blocks at each stage
- Graceful degradation (skip failed cities, continue pipeline)
- Detailed logging for debugging

### Production Practices
- Structured logging (file + console)
- Environment-based configuration
- Connection pooling considerations
- Batch inserts for efficiency

## 📈 Next Steps

**Week 2 (Dec 12-18):**
- [ ] Deploy to AWS Lambda
- [ ] Set up EventBridge scheduling
- [ ] Configure CloudWatch monitoring
- [ ] Add SNS alerting

**Week 3 (Dec 19-25):**
- [ ] Build Streamlit dashboard
- [ ] Deploy dashboard to Streamlit Cloud
- [ ] Add historical trend visualizations
- [ ] Create data quality dashboard

**Week 4+ (Future Enhancements):**
- [ ] Add more data sources (air quality, pollen)
- [ ] Implement data quality anomaly detection
- [ ] Build predictive models
- [ ] Add Terraform for IaC

## 💰 Cost Analysis

**Current Monthly Costs:**
- RDS db.t3.micro: ~$15/month (free for first 12 months)
- Lambda: ~$0.20/month (well within free tier)
- Data transfer: ~$0.50/month
- **Total: ~$0.70/month** (after free tier applied)

## 🤝 Background Context

Built by a Senior Database Analyst with 25+ years in data warehousing, transitioning from traditional ETL to modern cloud-native data engineering. This project demonstrates:

- **AWS Solutions Architect Associate** certification in practice
- **SRE Foundation** principles (SLIs, error budgets, monitoring)
- Python in production (beyond coursework)
- Cloud-native architecture design

## 📫 Contact

**Ben Schwab**
- Email: benjamin.schwab11@gmail.com
- LinkedIn: [Your LinkedIn]
- Location: San Diego, CA

---

**Last Updated:** December 11, 2024  
**Status:** ✅ Active Development - Week 1 Complete

