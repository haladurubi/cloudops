
variable "subscription_id" {
  description = "Azure subscription for CloudOps"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "polandcentral"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "dev"
}

variable "acr_name" {
  description = "Globally unique Azure Container Registry name"
  type        = string
  default     = "acrcloudopsfa8376b2"
}

