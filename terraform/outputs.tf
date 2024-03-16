output "container_latest_revision_fqdn" {
  description = "The fully qualified domain name (FQDN) of the container app, click to view"
  value       = azurerm_container_app.platform.latest_revision_fqdn
}
