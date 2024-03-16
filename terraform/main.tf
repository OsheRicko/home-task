provider "azurerm" {
  features {}
  skip_provider_registration = true
}

# terraform import azurerm_resource_group.built_in /subscriptions/2837fa98-ba70-4d44-a7e7-730ceb335460/resourceGroups/osher-rg

data "azurerm_client_config" "current" {}

resource "azurerm_resource_group" "built_in" {
  name     = "osher-rg"
  location = "West Europe"
}

resource "azurerm_log_analytics_workspace" "app_log_analytics" {
  name                = "assignment-app-log-analytics"
  location            = azurerm_resource_group.built_in.location
  resource_group_name = azurerm_resource_group.built_in.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_container_app_environment" "infrastructure" {
  name                       = var.container_environment_name
  location                   = azurerm_resource_group.built_in.location
  resource_group_name        = azurerm_resource_group.built_in.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.app_log_analytics.id
}

resource "azurerm_container_app" "platform" {
  name                         = var.container_app_name
  container_app_environment_id = azurerm_container_app_environment.infrastructure.id
  resource_group_name          = azurerm_resource_group.built_in.name
  revision_mode                = "Multiple"

  template {
    container {
      name   = "app-container"
      image  = var.container_image
      cpu    = var.container_cpu
      memory = var.container_memory
    }
  }

  ingress {
    allow_insecure_connections = false
    external_enabled           = true
    target_port                = 80
    transport                  = "http"
    traffic_weight {
      latest_revision = true
      percentage      = 50
    }
  }
}

resource "azurerm_mssql_server" "db_server" {
  name                         = "assignment-app-sql-server"
  resource_group_name          = azurerm_resource_group.built_in.name
  location                     = azurerm_resource_group.built_in.location
  administrator_login          = "sqluser"
  administrator_login_password = var.admin_password
  version                      = "12.0"
}

resource "azurerm_mssql_database" "db" {
  name      = "assignment-app-db"
  server_id = azurerm_mssql_server.db_server.id
  zone_redundant = true
}

resource "azurerm_key_vault" "keyvault" {
  name                        = "assignment-app-keyvault2"
  location                    = azurerm_resource_group.built_in.location
  resource_group_name         = azurerm_resource_group.built_in.name
  enabled_for_disk_encryption = true
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  sku_name                    = "standard"

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id

    secret_permissions = [
      "Get",
      "Set",
      "List",
    ]
  }
}
