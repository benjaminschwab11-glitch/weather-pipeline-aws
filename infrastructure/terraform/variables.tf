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

# Lambda Configuration
variable "lambda_function_name" {
  description = "Name of Lambda function"
  type        = string
  default     = "weather-pipeline"
}

variable "lambda_runtime" {
  description = "Lambda runtime"
  type        = string
  default     = "python3.11"
}

variable "lambda_timeout" {
  description = "Lambda timeout in seconds"
  type        = number
  default     = 30
}

variable "lambda_memory" {
  description = "Lambda memory in MB"
  type        = number
  default     = 128
}

variable "weather_api_key" {
  description = "OpenWeatherMap API key"
  type        = string
  sensitive   = true
}

variable "cities" {
  description = "Comma-separated list of cities"
  type        = string
  default     = "San Diego,Los Angeles,San Francisco,Seattle,Portland"
}

