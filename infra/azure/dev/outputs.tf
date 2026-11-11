
output "resource_group_name" {
  description = "CloudOps resource group name"
  value       = azurerm_resource_group.cloudops.name
}

output "resource_group_id" {
  description = "CloudOps resource group Azure ID"
  value       = azurerm_resource_group.cloudops.id
}

output "virtual_network_name" {
  description = "CloudOps virtual network"
  value       = azurerm_virtual_network.cloudops.name
}

output "virtual_network_id" {
  description = "CloudOps virtual network ID"
  value       = azurerm_virtual_network.cloudops.id
}

output "aks_subnet_id" {
  description = "Subnet reserved for AKS"
  value       = azurerm_subnet.aks.id
}

output "acr_name" {
  description = "CloudOps container registry name"
  value       = azurerm_container_registry.cloudops.name
}

output "acr_login_server" {
  description = "Container registry login server"
  value       = azurerm_container_registry.cloudops.login_server
}

