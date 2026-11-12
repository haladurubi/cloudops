locals {
  ecs_image = "${aws_ecr_repository.cloudops.repository_url}:v2"

  ecs_logs = {
    logDriver = "awslogs"
    options = {
      "awslogs-group"         = aws_cloudwatch_log_group.ecs.name
      "awslogs-region"        = "eu-north-1"
      "awslogs-stream-prefix" = "cloudops"
    }
  }

  ecs_mounts = [{
    sourceVolume  = "cloudops-data"
    containerPath = "/data"
    readOnly      = false
  }]
}

resource "aws_ecs_task_definition" "cloudops" {
  family                   = "cloudops-dev"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"

  cpu    = "512"
  memory = "1024"

  execution_role_arn = aws_iam_role.ecs_execution.arn

  runtime_platform {
    operating_system_family = "LINUX"
    cpu_architecture        = "X86_64"
  }

  volume {
    name = "cloudops-data"
  }

  container_definitions = jsonencode([
    {
      name       = "init-data"
      image      = local.ecs_image
      essential  = false
      user       = "0"
      entryPoint = ["sh", "-c"]
      command    = ["chown cloudops:cloudops /data"]

      mountPoints      = local.ecs_mounts
      logConfiguration = local.ecs_logs
    },
    {
      name      = "api"
      image     = local.ecs_image
      essential = true

      portMappings = [{
        containerPort = 8000
        protocol      = "tcp"
      }]

      dependsOn = [{
        containerName = "init-data"
        condition     = "SUCCESS"
      }]

      environment = [{
        name  = "DATABASE_URL"
        value = "sqlite:////data/cloudops.db"
      }]

      mountPoints = local.ecs_mounts

      healthCheck = {
        command = [
          "CMD-SHELL",
          "python -c 'import urllib.request; urllib.request.urlopen(\"http://127.0.0.1:8000/health\", timeout=3)'"
        ]
        interval    = 30
        timeout     = 5
        retries     = 3
        startPeriod = 15
      }

      logConfiguration = local.ecs_logs
    },
    {
      name      = "worker"
      image     = local.ecs_image
      essential = true

      command = [
        "python", "-u", "-m", "app.worker",
        "--interval", "15"
      ]

      dependsOn = [
        {
          containerName = "init-data"
          condition     = "SUCCESS"
        },
        {
          containerName = "api"
          condition     = "HEALTHY"
        }
      ]

      environment = [
        {
          name  = "DATABASE_URL"
          value = "sqlite:////data/cloudops.db"
        },
        {
          name  = "MONITOR_TARGET_URL"
          value = "http://127.0.0.1:8000/health"
        }
      ]

      mountPoints      = local.ecs_mounts
      logConfiguration = local.ecs_logs
    }
  ])
}
