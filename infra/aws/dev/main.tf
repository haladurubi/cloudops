provider "aws" {
  region  = "eu-north-1"
  profile = "cloudops"

  default_tags {
    tags = {
      Project     = "CloudOps"
      Environment = "dev"
      ManagedBy   = "Terraform"
    }
  }
}
