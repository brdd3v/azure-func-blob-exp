resource "azurerm_resource_group" "rg" {
  name     = "resource-group-exp"
  location = "Germany West Central"
}

resource "azurerm_storage_account" "sa" {
  name                     = "saccount01exp"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_container" "container" {
  name                 = "container-exp"
  storage_account_name = azurerm_storage_account.sa.name
}

resource "azurerm_service_plan" "sp" {
  name                = "service-plan-exp"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  os_type             = "Linux"
  sku_name            = "B1"
}

resource "azurerm_linux_function_app" "linux_func" {
  name                = "linux-function-app-exp"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  service_plan_id     = azurerm_service_plan.sp.id

  storage_account_name       = azurerm_storage_account.sa.name
  storage_account_access_key = azurerm_storage_account.sa.primary_access_key

  zip_deploy_file = data.archive_file.code.output_path

  site_config {
    application_stack {
      python_version = "3.10"
    }
  }

  app_settings = {
    SCM_DO_BUILD_DURING_DEPLOYMENT = true
    ENABLE_ORYX_BUILD              = true
    FUNCTIONS_WORKER_RUNTIME       = "python"
  }
}

data "archive_file" "code" {
  type        = "zip"
  source_dir  = "${path.module}/../code"
  output_path = "${path.module}/../code.zip"
}
