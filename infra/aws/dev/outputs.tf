output "vpc_id" {
  description = "ID of the CloudOps VPC"
  value       = aws_vpc.cloudops.id
}

output "ecr_repository_url" {
  description = "AWS ECR repository URL for CloudOps"
  value       = aws_ecr_repository.cloudops.repository_url
}
