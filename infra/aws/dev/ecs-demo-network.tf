resource "aws_security_group" "ecs_demo" {
  name        = "cloudops-ecs-demo-dev"
  description = "Security group for short-lived CloudOps ECS demo"
  vpc_id      = aws_vpc.cloudops.id

  tags = {
    Name = "cloudops-ecs-demo-dev"
  }
}

resource "aws_vpc_security_group_egress_rule" "ecs_https" {
  security_group_id = aws_security_group.ecs_demo.id

  description = "Allow outbound HTTPS for ECR and CloudWatch"
  ip_protocol = "tcp"
  from_port   = 443
  to_port     = 443
  cidr_ipv4   = "0.0.0.0/0"
}

output "ecs_demo_security_group_id" {
  value = aws_security_group.ecs_demo.id
}

output "ecs_demo_public_subnet_id" {
  value = aws_subnet.public[0].id
}
