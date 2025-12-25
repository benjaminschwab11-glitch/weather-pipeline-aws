# Main Terraform configuration
# This file serves as the entry point

# Data source for AWS account ID
data "aws_caller_identity" "current" {}

# Data source for default VPC (RDS uses it)
data "aws_vpc" "default" {
  default = true
}

# Local values
locals {
  account_id = data.aws_caller_identity.current.account_id
  vpc_id     = data.aws_vpc.default.id
}

