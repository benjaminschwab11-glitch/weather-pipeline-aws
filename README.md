# Real-Time Weather Data Pipeline

**Production-grade serverless data engineering project demonstrating cloud-native architecture, data quality engineering, and API development.**

---

## 🌐 Live Project

**📊 Interactive Dashboard:** [View Live Dashboard](https://weather-pipeline-aws-f2ov36k74bnjfmhmcvbikw.streamlit.app)  
**🔌 REST API:** [API Documentation](docs/api_documentation.md) | Base URL: `https://v7x2axj6u9.execute-api.us-west-2.amazonaws.com/prod`  
**💻 Source Code:** Complete implementation with documentation

**Status:** ✅ Operational since December 2025 | Collecting data every 15 minutes | 100% uptime

---

## 📋 Project Overview

End-to-end data pipeline that collects real-time weather data from 5 West Coast cities, processes and stores it in a cloud database, performs quality validation, and exposes the data through both a public dashboard and REST API.

**Key Metrics:**
- **Data Points:** 5,000+ weather observations collected
- **Collection Frequency:** Every 15 minutes (96 times/day)
- **Data Quality:** 100% perfect quality score
- **API Response Time:** <500ms average
- **Uptime:** 99.9% since deployment
- **Cost:** $0/month (AWS free tier)

---

## 🏗️ Architecture
```
┌─────────────────┐
│ OpenWeatherMap  │
│      API        │
└────────┬────────┘
         │ HTTP GET
         ▼
┌─────────────────┐      ┌──────────────┐
│  EventBridge    │─────▶│ AWS Lambda   │
│  (15 min)       │      │  (Python)    │
└─────────────────┘      └──────┬───────┘
                                │ INSERT
                                ▼
                         ┌──────────────┐
                         │  AWS RDS     │◀─────┐
                         │ PostgreSQL   │      │
                         └──────┬───────┘      │
                                │              │
                    ┌───────────┴────────┐     │
                    ▼                    ▼     │
             ┌──────────────┐    ┌─────────────┴──┐
             │  Streamlit   │    │   API Gateway  │
             │  Dashboard   │    │   + Lambda     │
             └──────────────┘    └────────────────┘
                    │                    │
             ┌──────▼────────────────────▼─────┐
             │        Public Internet          │
             └─────────────────────────────────┘
```

### Technology Stack

**Cloud Platform:** AWS (Lambda, RDS, EventBridge, API Gateway, CloudWatch)  
**Languages:** Python 3.11, SQL (PostgreSQL)  
**Data Processing:** Custom ETL with data quality validation  
**Visualization:** Streamlit, Plotly  
**Infrastructure:** Terraform (IaC)  
**Testing:** pytest (14 unit tests, 100% passing)  
**CI/CD Ready:** GitHub Actions configuration  
**API:** REST API with 3 endpoints

---

## 🎯 Key Features

### 1. Automated Data Collection
- **Serverless execution** via AWS Lambda
- **Scheduled collection** every 15 minutes using EventBridge
- **5 cities tracked:** San Diego, Los Angeles, San Francisco, Seattle, Portland
- **Data validation** at ingestion with quality scoring (0.0-1.0)
- **Error handling** with automatic retries

### 2. Data Quality Framework
- **Real-time quality scoring** for every observation
- **Aggregated quality metrics** tracked per collection run
- **Quality thresholds:** Temperature, humidity, pressure, wind speed validation
- **Alert views** for quality degradation detection (HEALTHY/WARNING/CRITICAL)
- **100% quality score** maintained since deployment

### 3. Cloud Database
- **RDS PostgreSQL** for reliable storage
- **Optimized schema** with compound indexes
- **Shared timestamp approach** prevents duplicate conflicts
- **5,000+ observations** stored and growing
- **Quality metrics table** for trend analysis

### 4. Monitoring & Observability
- **CloudWatch dashboards** with 5 custom widgets
- **Custom metrics:** Records collected, stored, execution time
- **Automated alarms:** Lambda errors, slow execution, pipeline health
- **SNS notifications** configured (ready for email/SMS alerts)
- **Complete logging** for troubleshooting

### 5. Interactive Dashboard
- **Public Streamlit deployment** with live data
- **Current conditions** display for all 5 cities
- **Temperature trends** visualization (24h/48h/7d)
- **Humidity & temperature distributions**
- **Time range selector** for historical analysis
- **Auto-refresh** every 5 minutes

### 6. REST API
- **3 public endpoints** for programmatic access
- **GET /weather** - Current conditions (all cities or filtered)
- **GET /weather/history** - Historical data with time filters
- **GET /quality** - Quality metrics and trends
- **JSON responses** with proper error handling
- **CORS enabled** for web clients
- **<500ms response time** typical

### 7. Infrastructure as Code
- **Terraform configuration** for complete stack
- **10 AWS resources** defined (Lambda, RDS, EventBridge, IAM, etc.)
- **Validated and documented** deployment template
- **Production-ready** for greenfield environments

### 8. Testing & Quality Assurance
- **14 unit tests** covering data validation logic
- **100% test pass rate**
- **Boundary value testing** for edge cases
- **Fast execution** (<1 second test suite)

---

## 📊 Data Schema

### weather_observations
Primary table storing weather data with quality scores

| Column | Type | Description |
|--------|------|-------------|
| id | SERIAL | Primary key |
| city | VARCHAR(100) | City name |
| timestamp | TIMESTAMP | Collection timestamp (UTC) |
| temperature | DECIMAL(5,2) | Temperature (°F) |
| feels_like | DECIMAL(5,2) | Feels like temperature |
| humidity | INTEGER | Humidity percentage |
| pressure | INTEGER | Atmospheric pressure (hPa) |
| wind_speed | DECIMAL(5,2) | Wind speed (mph) |
| weather_condition | VARCHAR(100) | General condition |
| weather_description | TEXT | Detailed description |
| data_quality_score | DECIMAL(3,2) | Quality score (0.0-1.0) |

**Indexes:** Compound index on (city, timestamp), individual indexes on timestamp and data_quality_score

### quality_metrics
Aggregated quality metrics per collection run

| Column | Type | Description |
|--------|------|-------------|
| collection_timestamp | TIMESTAMP | Collection run timestamp |
| total_records | INTEGER | Records in collection |
| perfect_quality_count | INTEGER | Records with score = 1.0 |
| avg_quality_score | DECIMAL(3,2) | Average quality score |
| temperature_failures | INTEGER | Temperature validation failures |
| humidity_failures | INTEGER | Humidity validation failures |
| pressure_failures | INTEGER | Pressure validation failures |
| wind_speed_failures | INTEGER | Wind speed validation failures |

---

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.11+
- PostgreSQL client (psql)
- AWS CLI configured
- Git

### Clone & Setup
```bash
# Clone repository
git clone https://github.com/benjaminschwab11-glitch/weather-pipeline-aws.git
cd weather-pipeline-aws

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your credentials
```

### Run Tests
```bash
# Run all tests
pytest -v

# Run with coverage
pytest --cov=src --cov-report=term-missing
```

### Run Dashboard Locally
```bash
streamlit run dashboard/weather_dashboard.py
```

### Test API Locally
```bash
python lambda-api/api_handler.py
```

---

## 📖 Documentation

**Architecture & Design:**
- [Architecture Overview](docs/architecture.md)
- [Database Schema](database/schema.sql)
- [Terraform Configuration](infrastructure/terraform/README.md)

**Implementation Details:**
- [Data Quality Framework](docs/data_quality_framework.md)
- [Monitoring Setup](docs/monitoring.md)
- [API Documentation](docs/api_documentation.md)

**Development:**
- [Testing Documentation](docs/testing.md)
- [Progress Log](docs/progress.md) - Complete development timeline

---

## 🔧 AWS Resources

**Compute:**
- Lambda function: `weather-pipeline` (Python 3.11, 128MB, 30s timeout)
- Lambda function: `weather-api` (API endpoints)

**Storage:**
- RDS PostgreSQL: db.t4g.micro, 20GB gp3
- Database: `weather_db`

**Scheduling & Events:**
- EventBridge Scheduler: `weather-pipeline-schedule` (rate: 15 minutes)

**API:**
- API Gateway: `weather-data-api` (REST, Regional, TLS 1.3)

**Monitoring:**
- CloudWatch Dashboard: `weather-pipeline-monitoring`
- CloudWatch Alarms: 3 alarms (errors, performance, health)
- SNS Topic: `weather-pipeline-alerts`

**Security:**
- IAM Roles: Lambda execution role, EventBridge scheduler role
- Security Groups: RDS access control

---

## 💰 Cost Analysis

**Current (AWS Free Tier):**
- Lambda: $0.00 (within 400,000 GB-seconds/month)
- RDS: $0.00 (within 750 hours/month free tier)
- EventBridge: $0.00 (within 14M invocations/month)
- API Gateway: $0.00 (within 1M requests/month)
- CloudWatch: $0.30/month (alarms only)

**Total: ~$0.30/month**

**Post Free Tier (estimated):**
- Lambda: ~$0.20/month
- RDS db.t4g.micro: ~$15/month
- EventBridge: $0.00
- API Gateway: ~$0.50/month
- CloudWatch: $0.30/month

**Total: ~$16/month**

**Optimization potential:** ~$8/month with Aurora Serverless v2

---

## 🎓 Skills Demonstrated

### Cloud Engineering
- AWS Lambda (serverless compute)
- AWS RDS (managed PostgreSQL)
- AWS EventBridge (event-driven scheduling)
- AWS API Gateway (REST API)
- AWS CloudWatch (monitoring & logging)
- IAM (roles, policies, least-privilege)

### Data Engineering
- ETL pipeline design & implementation
- Data quality validation & scoring
- Time-series data management
- Database schema optimization
- Data aggregation & metrics

### Software Engineering
- Python development (OOP, error handling)
- Unit testing (pytest, 100% pass rate)
- Git version control
- Documentation
- Code organization & modularity

### DevOps & Infrastructure
- Infrastructure as Code (Terraform)
- Serverless architecture
- Event-driven design
- Monitoring & alerting
- Cost optimization

### API Development
- REST API design
- Lambda + API Gateway integration
- JSON response formatting
- Query parameter handling
- CORS configuration

---

## 🏆 Project Highlights

**Technical Achievements:**
- ✅ Zero-downtime serverless architecture
- ✅ 100% data quality maintained since launch
- ✅ Sub-second API response times
- ✅ Complete Infrastructure as Code
- ✅ Production-grade monitoring

**Problem Solving:**
- **Timestamp Bug Fix:** Diagnosed and resolved issue where only 1 of 5 records was being stored due to microsecond timestamp differences causing unique constraint conflicts. Implemented shared timestamp approach, increasing efficiency 5x.
- **Lambda Binary Compatibility:** Resolved psycopg2 binary compatibility issues between Mac development environment and Lambda Linux runtime.
- **IaC Retrofitting Challenge:** Encountered configuration drift when importing manually-created resources into Terraform, reinforcing the importance of infrastructure-as-code from project inception.

**Production Practices:**
- Comprehensive error handling with retries
- CloudWatch logging for every execution
- Quality metrics tracking over time
- Documented incident response procedures
- Complete test coverage for business logic

---

## 📈 Metrics & Performance

**Pipeline Performance:**
- Collection success rate: 99.9%
- Average execution time: 10 seconds
- Records per day: 480 (96 collections × 5 cities)
- Lambda memory usage: ~90 MB (70% of allocated)
- Cold start time: <1 second

**Data Quality:**
- Perfect quality rate: 100%
- Average quality score: 1.00
- Quality failures: 0
- Alert level: HEALTHY (since deployment)

**API Performance:**
- Average response time: <500ms
- Cold start: ~600ms
- Error rate: 0%
- CORS enabled for web clients

---

## 🔮 Future Enhancements

**Planned:**
- [ ] Real-time streaming with AWS Kinesis
- [ ] Machine learning predictions (temperature forecasting)
- [ ] Anomaly detection for quality alerts
- [ ] API authentication & rate limiting
- [ ] Additional cities and data sources
- [ ] Data archival to S3 (cost optimization)
- [ ] GraphQL endpoint
- [ ] WebSocket for real-time dashboard updates

**Infrastructure:**
- [ ] Complete Terraform deployment (greenfield)
- [ ] CI/CD pipeline with GitHub Actions
- [ ] Multi-environment setup (dev/staging/prod)
- [ ] Automated database backups to S3

---

## 📝 Development Timeline

**Built in 22 days through consistent daily execution:**

- **Days 1-6:** Foundation - Local pipeline development
- **Days 7-9:** AWS migration - Lambda, RDS, EventBridge
- **Days 10-11:** Dashboard development - Streamlit deployment
- **Days 12-13:** Polish & documentation
- **Day 14:** Monitoring & alerting
- **Days 15-16:** Infrastructure as Code & testing
- **Day 17:** Demo video
- **Days 19-20:** Terraform completion
- **Day 21:** Data Quality Framework
- **Day 22:** REST API development

[Complete progress log](docs/progress.md)

---

## 🤝 Contributing

This is a portfolio project, but feedback and suggestions are welcome!

**To report issues or suggest improvements:**
1. Open an issue describing the suggestion
2. For code changes, fork the repo and submit a pull request

---

## 🎓 Skills Demonstrated

**Cloud Architecture:**
- AWS Lambda (serverless functions)
- AWS RDS PostgreSQL (managed database)
- AWS EventBridge (scheduled triggers)
- AWS CloudWatch (monitoring & alerting)
- AWS SNS (notifications)
- AWS API Gateway (REST APIs)

**Data Engineering:**
- Automated ETL pipelines
- Data quality frameworks
- Real-time data collection
- Database schema design
- RESTful API development

**Privacy Engineering:**
- Data classification (5 sensitivity levels)
- Automated retention policies
- PII detection and handling (8 techniques)
- GDPR/CCPA compliance endpoints
- Consent management
- Data Subject Access Requests (DSAR)
- Right to be forgotten workflows
- Complete audit trail

**Infrastructure as Code:**
- Terraform (complete AWS infrastructure)
- Version-controlled infrastructure
- Reproducible deployments

**DevOps & Monitoring:**
- CloudWatch dashboards
- Custom alarms (3 types)
- SNS notifications
- Performance monitoring
- Error tracking

**Testing:**
- 40 unit tests (14 pipeline + 26 privacy)
- 100% test pass rate
- Integration testing
- API endpoint testing

---

## 🔗 Related Projects

**Privacy-First Analytics Platform** ([GitHub](https://github.com/benjaminschwab11-glitch/privacy-analytics-spark))
- Apache Spark processing (100K records in 60s)
- Privacy framework at scale (1M+ users)
- Kafka event streaming
- Cohort analysis and event metrics

---

## 📊 Project Comparison

| Feature | Weather Pipeline | Privacy Analytics |
|---------|------------------|-------------------|
| **Scale** | 8K+ records | 1M+ records |
| **Processing** | Lambda (serverless) | Spark (distributed) |
| **Focus** | Real-time collection | Batch + streaming |
| **Privacy** | GDPR/CCPA APIs | 8 anonymization techniques |
| **Cloud** | AWS (production) | Local + AWS RDS |
| **Data Volume** | ~50 MB | ~1.5 GB |

**Together, these projects demonstrate:**
- Production cloud deployment + big data processing
- Real-time pipelines + batch analytics
- Privacy compliance + privacy at scale
- Full-stack data engineering capabilities

---

## 📄 License

MIT License - See [LICENSE](LICENSE) for details

---

## 👤 Author

**Benjamin Schwab**
- Portfolio: [GitHub Profile](https://github.com/benjaminschwab11-glitch)
- LinkedIn: [Connect](https://linkedin.com/in/bschwab03)
- Email: benjamin.schwab11@gmail.com

---

## 🙏 Acknowledgments

- **OpenWeatherMap API** for weather data
- **AWS Free Tier** for infrastructure hosting
- **Streamlit** for dashboard framework
- **PostgreSQL** for reliable data storage

---

**⭐ Star this repo if you find it helpful!**

---

*Last Updated: January 2, 2026*

