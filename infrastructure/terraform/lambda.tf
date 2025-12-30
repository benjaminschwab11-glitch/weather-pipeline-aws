# Data source for Lambda deployment package
# Note: This assumes you have a pre-built deployment package
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../../lambda/package"
  output_path = "${path.module}/lambda_deployment.zip"
  excludes    = ["__pycache__", "*.pyc"]
}

# Lambda Function
resource "aws_lambda_function" "weather_pipeline" {
  function_name = var.lambda_function_name
  role          = aws_iam_role.lambda_role.arn
  
  # Deployment package
  filename         = data.archive_file.lambda_zip.output_path
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  
  # Runtime configuration
  runtime = var.lambda_runtime
  handler = "lambda_function.lambda_handler"
  timeout = var.lambda_timeout
  memory_size = var.lambda_memory
  
  # Environment variables
  environment {
    variables = {
      WEATHER_API_KEY = var.weather_api_key
      CITIES          = var.cities
      RDS_ENDPOINT    = aws_db_instance.weather_db.address
      RDS_DATABASE    = var.db_name
      RDS_USERNAME    = var.db_username
      RDS_PASSWORD    = var.db_password
      RDS_PORT        = "5432"
    }
  }
  
  # VPC configuration (optional - only if Lambda needs to be in VPC)
  # Commenting out since your RDS is publicly accessible
  # vpc_config {
  #   subnet_ids         = [...]
  #   security_group_ids = [...]
  # }
  
  tags = {
    Name = "${var.project_name}-lambda"
  }
}

# CloudWatch Log Group for Lambda
resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/${var.lambda_function_name}"
  retention_in_days = 7
  
  tags = {
    Name = "${var.project_name}-lambda-logs"
  }
}

# Lambda outputs
output "lambda_function_arn" {
  description = "ARN of Lambda function"
  value       = aws_lambda_function.weather_pipeline.arn
}

output "lambda_function_name" {
  description = "Name of Lambda function"
  value       = aws_lambda_function.weather_pipeline.function_name
}

output "lambda_function_invoke_arn" {
  description = "Invoke ARN for Lambda function"
  value       = aws_lambda_function.weather_pipeline.invoke_arn
}

