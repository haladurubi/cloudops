
resource "azurerm_container_registry" "cloudops" {
  name                = var.acr_name
  resource_group_name = azurerm_resource_group.cloudops.name
  location            = azurerm_resource_group.cloudops.location

  sku           = "Basic"
  admin_enabled = false

  public_network_access_enabled = true

  tags = {
    project     = "CloudOps"
    environment = var.environment
    managed_by  = "terraform"
  }
}
