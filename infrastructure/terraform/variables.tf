# AWS Region
variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-west-2"
}

# Project name
variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "weather-pipeline"
}

# RDS Configuration
variable "db_name" {
  description = "PostgreSQL database name"
  type        = string
  default     = "weather_db"
}

variable "db_username" {
  description = "PostgreSQL master username"
  type        = string
  default     = "weather_admin"
  sensitive   = true
}

variable "db_password" {
  description = "PostgreSQL master password"
  type        = string
  sensitive   = true
}

variable "db_instance_class" {
  description = "RDS instance class"
  type        = string
  default     = "db.t3.micro"
}

variable "db_allocated_storage" {
  description = "Allocated storage in GB"
  type        = number
  default     = 20
}

# Security - allowed IP for database access
variable "allowed_cidr_blocks" {
  description = "CIDR blocks allowed to access RDS"
  type        = list(string)
  default     = ["0.0.0.0/0"] # WARNING: Open to world - for portfolio only
}

