# Security Group for RDS
resource "aws_security_group" "rds_sg" {
  name        = "${var.project_name}-rds-sg"
  description = "Security group for weather pipeline RDS PostgreSQL"
  
  ingress {
    description = "PostgreSQL access"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = var.allowed_cidr_blocks
  }
  
  egress {
    description = "Allow all outbound"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "${var.project_name}-rds-sg"
  }
}

# RDS PostgreSQL Instance
resource "aws_db_instance" "weather_db" {
  identifier     = "${var.project_name}-db"
  engine         = "postgres"
  engine_version = "15.15"  # Match actual version
  
  instance_class    = "db.t4g.micro"  # Match actual (ARM-based)
  allocated_storage = var.db_allocated_storage
  storage_type      = "gp3"  # Match actual (gp3 not gp2)
  iops              = 3000   # gp3 default
  storage_throughput = 125   # gp3 default
  
  db_name  = var.db_name
  username = var.db_username
  password = var.db_password
  
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  publicly_accessible    = true
  
  backup_retention_period = 1
  backup_window          = "11:38-12:08"  # Match actual
  maintenance_window     = "sat:06:40-sat:07:10"  # Match actual
  
  copy_tags_to_snapshot = true  # Match actual
  
  skip_final_snapshot       = true
  deletion_protection       = false
  
  # Allow Terraform to manage these
  apply_immediately = false
  
  tags = {
    Name = "${var.project_name}-postgres"
  }
  
  lifecycle {
    ignore_changes = [
      password,  # Don't force password change
      engine_version,  # Allow minor version upgrades
    ]
  }
}

