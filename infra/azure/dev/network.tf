
resource "azurerm_virtual_network" "cloudops" {
  name                = "vnet-cloudops-${var.environment}"
  location            = azurerm_resource_group.cloudops.location
  resource_group_name = azurerm_resource_group.cloudops.name
  address_space       = ["10.20.0.0/16"]

  tags = {
    project     = "CloudOps"
    environment = var.environment
    managed_by  = "terraform"
  }
}

resource "azurerm_subnet" "aks" {
  name                 = "snet-aks-${var.environment}"
  resource_group_name  = azurerm_resource_group.cloudops.name
  virtual_network_name = azurerm_virtual_network.cloudops.name
  address_prefixes     = ["10.20.1.0/24"]
}
