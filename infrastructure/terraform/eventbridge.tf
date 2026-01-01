# Lambda permission for EventBridge to invoke
resource "aws_lambda_permission" "eventbridge_invoke" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.weather_pipeline.function_name
  principal     = "scheduler.amazonaws.com"
  source_arn    = aws_scheduler_schedule.weather_pipeline.arn
}

# EventBridge Scheduler Schedule
resource "aws_scheduler_schedule" "weather_pipeline" {
  name        = var.schedule_name
  description = var.schedule_description

  # Schedule configuration
  schedule_expression = var.schedule_expression

  # Flexible time window (off for exact timing)
  flexible_time_window {
    mode = "OFF"
  }

  # Target: Lambda function
  target {
    arn      = aws_lambda_function.weather_pipeline.arn
    role_arn = aws_iam_role.eventbridge_role.arn

    # Retry policy
    retry_policy {
      maximum_retry_attempts       = 185
      maximum_event_age_in_seconds = 86400 # 24 hours
    }
  }

  # State: Enabled
  state = "ENABLED"
}

# Outputs
output "schedule_name" {
  description = "Name of EventBridge schedule"
  value       = aws_scheduler_schedule.weather_pipeline.name
}

output "schedule_arn" {
  description = "ARN of EventBridge schedule"
  value       = aws_scheduler_schedule.weather_pipeline.arn
}

output "schedule_state" {
  description = "State of EventBridge schedule"
  value       = aws_scheduler_schedule.weather_pipeline.state
}

