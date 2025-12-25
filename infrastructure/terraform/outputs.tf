# RDS Endpoint
output "rds_endpoint" {
  description = "RDS instance endpoint"
  value       = aws_db_instance.weather_db.endpoint
}

# RDS Address
output "rds_address" {
  description = "RDS instance address (hostname only)"
  value       = aws_db_instance.weather_db.address
}

# RDS Port
output "rds_port" {
  description = "RDS instance port"
  value       = aws_db_instance.weather_db.port
}

# Database Name
output "database_name" {
  description = "Database name"
  value       = aws_db_instance.weather_db.db_name
}

# Security Group ID
output "rds_security_group_id" {
  description = "Security group ID for RDS"
  value       = aws_security_group.rds_sg.id
}

