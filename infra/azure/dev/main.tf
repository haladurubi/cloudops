
resource "azurerm_resource_group" "cloudops" {
  name     = "rg-cloudops-${var.environment}"
  location = var.location

  tags = {
    project     = "CloudOps"
    environment = var.environment
    managed_by  = "terraform"
  }
}
