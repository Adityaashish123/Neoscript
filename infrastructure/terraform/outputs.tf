output "instance_id" {
  description = "EC2 Instance ID"
  value       = aws_instance.api_server.id
}

output "public_ip" {
  description = "Public IP address"
  value       = aws_instance.api_server.public_ip
}

output "api_endpoint" {
  description = "API Endpoint URL"
  value       = "http://${aws_instance.api_server.public_ip}:5000"
}

output "log_group_name" {
  description = "CloudWatch Log Group"
  value       = aws_cloudwatch_log_group.api_logs.name
}