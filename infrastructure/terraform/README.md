# Terraform Infrastructure as Code

**Status:** Configuration created, import attempted  
**Created:** December 25, 2024

## Overview

This directory contains Terraform configuration to define the weather pipeline infrastructure as code. The configuration defines RDS PostgreSQL and security groups with proper tagging and settings.

## Files

- **providers.tf** - AWS provider configuration, Terraform version requirements
- **variables.tf** - Input variables for configuration
- **terraform.tfvars** - Variable values (gitignored - contains secrets)
- **main.tf** - Main configuration, data sources
- **rds.tf** - RDS PostgreSQL database and security group definitions
- **outputs.tf** - Output values (endpoints, IDs)

## Configuration

### Defined Resources

**RDS PostgreSQL:**
- Identifier: `weather-pipeline-db`
- Engine: PostgreSQL 15.15
- Instance: db.t4g.micro (ARM-based)
- Storage: 20GB gp3 (3000 IOPS, 125 MB/s throughput)
- Backup retention: 1 day
- Public access: Yes (for portfolio demonstration)

**Security Group:**
- Name: `weather-pipeline-rds-sg`
- Inbound: PostgreSQL (5432) from 0.0.0.0/0
- Outbound: All traffic

### Variables

Key variables in `variables.tf`:
- `aws_region` - AWS region (default: us-west-2)
- `project_name` - Project identifier
- `db_name`, `db_username`, `db_password` - Database credentials
- `db_instance_class`, `db_allocated_storage` - Database sizing
- `allowed_cidr_blocks` - Network access control

## Usage

### Prerequisites
```bash
# Install Terraform
brew install terraform

# Configure AWS CLI
aws configure
```

### Initialize
```bash
# Initialize Terraform (downloads providers)
terraform init
```

### Plan
```bash
# Preview changes
terraform plan
```

### Apply (Not Recommended for Existing Infrastructure)
```bash
# WARNING: This would create NEW resources
# Existing resources should be imported first
terraform apply
```

## Current Status: Import Challenges

**Attempted:** Import of existing RDS and security group into Terraform state

**Challenge:** Existing resources have immutable attributes that differ from Terraform configuration:
- RDS encryption settings
- Security group name and description
- These differences force resource replacement (destroy + recreate)

**Resolution Options:**

1. **Accept configuration as documentation** - IaC files demonstrate understanding without managing existing resources
2. **Create parallel infrastructure** - Use Terraform to deploy fresh resources with different names
3. **Manual state editing** - Advanced technique to align state with existing resources

**Current Approach:** Configuration files serve as IaC documentation and template for future deployments.

## What Was Learned

**Terraform Workflow:**
- `terraform init` - Initialize project
- `terraform plan` - Preview changes
- `terraform import` - Import existing resources
- `terraform state` - Manage state

**Key Concepts:**
- Declarative infrastructure definition
- State management
- Resource dependencies
- Provider configuration
- Variable management with sensitive values

**Real-World Challenges:**
- Importing existing infrastructure is complex
- Some resource attributes are immutable
- Manual console deployments vs. IaC from start
- State file contains actual infrastructure details

## For Production Deployment

**Recommended approach for new environments:**
```bash
# 1. Initialize
terraform init

# 2. Plan
terraform plan -out=tfplan

# 3. Review plan carefully

# 4. Apply
terraform apply tfplan

# 5. Save state securely
# Consider: Terraform Cloud, S3 backend with state locking
```

## Security Notes

**⚠️ Important:**
- `terraform.tfvars` contains secrets - never commit to git
- `.gitignore` excludes: `*.tfvars`, `terraform.tfstate*`, `.terraform/`
- State files contain sensitive data - store securely
- Current config allows public RDS access (0.0.0.0/0) - acceptable for portfolio, not production

## Future Enhancements

**To complete IaC coverage:**
- [ ] Add Lambda function resource
- [ ] Add EventBridge schedule
- [ ] Add CloudWatch alarms
- [ ] Add SNS topic
- [ ] Use remote state backend (S3 + DynamoDB)
- [ ] Implement CI/CD pipeline
- [ ] Add modules for reusability
- [ ] Separate environments (dev/staging/prod)

## Cost

**Terraform itself:** Free (open source)

**AWS resources defined:**
- RDS db.t4g.micro: $0/month (free tier first 12 months)
- After free tier: ~$15/month

## References

- [Terraform AWS Provider](https://registry.terraform.io/providers/hashicorp/aws/latest/docs)
- [Terraform Import](https://developer.hashicorp.com/terraform/cli/import)
- [AWS RDS Terraform](https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/db_instance)

## Lambda Infrastructure Added (Day 19)

**Completed:** December 29, 2025

### New Resources Defined

**IAM Resources (`iam.tf`):**
- Lambda execution role with assume role policy
- AWS managed policy attachment (AWSLambdaBasicExecutionRole)
- Custom CloudWatch metrics policy
- Output: Lambda role ARN

**Lambda Resources (`lambda.tf`):**
- Lambda function with Python 3.11 runtime
- Automated deployment package creation (archive provider)
- Environment variable configuration
- CloudWatch log group (7-day retention)
- Outputs: Function ARN, name, invoke ARN

**Configuration:**
- Function name: weather-pipeline
- Runtime: Python 3.11
- Memory: 128 MB
- Timeout: 30 seconds
- Handler: lambda_function.lambda_handler

**Environment Variables (from Terraform):**
- WEATHER_API_KEY
- CITIES
- RDS_ENDPOINT (referenced from RDS resource)
- RDS_DATABASE, RDS_USERNAME, RDS_PASSWORD
- RDS_PORT

### Terraform Plan Results
```
Plan: 7 to add, 0 to change, 2 to destroy
```

**Resources to Add:**
1. aws_iam_role.lambda_role
2. aws_iam_role_policy.lambda_cloudwatch_metrics
3. aws_iam_role_policy_attachment.lambda_basic
4. aws_lambda_function.weather_pipeline
5. aws_cloudwatch_log_group.lambda_logs
6. (2 additional dependency resources)

**Why Not Applied:**

Existing RDS and security group resources have configuration drift from manual creation:
- Storage encryption settings
- Security group descriptions
- Resource naming

Terraform would destroy and recreate these (losing data). Since the database contains production data, apply was not executed.

**Learning:** This demonstrates the importance of Infrastructure as Code from project inception. Retrofitting IaC to manually-created resources is challenging due to:
- Immutable resource attributes
- Configuration drift
- State management complexity

### Production Deployment Approach

**For greenfield deployment (new environment):**
```bash
# Initialize
terraform init

# Plan
terraform plan -out=tfplan

# Review carefully
# Verify no existing resources will be destroyed

# Apply
terraform apply tfplan
```

**Current best practice:** Keep Lambda Terraform configuration as documentation and template for future deployments.

### Interview Talking Point

"I created complete Terraform configuration for the Lambda function, IAM roles, and CloudWatch logs. When attempting to integrate with existing manually-created RDS resources, I encountered configuration drift requiring resource replacement. This experience reinforced why infrastructure-as-code should be implemented from day one, not retrofitted. The configuration serves as a template for future deployments and demonstrates my understanding of IaC principles."

