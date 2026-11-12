terraform {
  backend "s3" {
    bucket       = "cloudops-tfstate-137e105140df1e65"
    key          = "cloudops/dev.tfstate"
    region       = "eu-north-1"
    profile      = "cloudops"
    encrypt      = true
    use_lockfile = true
  }
}
