locals {
  tags = {
    "environment" : "demo",
    "source" : "terraform"
  }
}
resource "azurerm_resource_group" "server" {
  name     = "server-rg"
  location = "Norway East"
}
resource "azurerm_virtual_network" "server" {
  name                = "cdktf-vnet"
  location            = azurerm_resource_group.server.location
  address_space       = ["10.0.0.0/16"]
  resource_group_name = azurerm_resource_group.server.name
  tags                = local.tags
}
resource "azurerm_subnet" "server" {
  name                 = "subnet1"
  resource_group_name  = azurerm_resource_group.server.name
  virtual_network_name = azurerm_virtual_network.server.name
  address_prefixes     = ["10.0.0.0/24"]
}
module "virtual_machine" {
  source  = "crayon/vm/azurerm"
  version = "1.10.1"

  name           = "server01"
  resource_group = azurerm_resource_group.server.name
  network_interface_subnets = [
    {
      name                 = azurerm_subnet.server.name
      virtual_network_name = azurerm_subnet.server.virtual_network_name
      resource_group_name  = azurerm_subnet.server.resource_group_name
      public_ip_id         = null
      static_ip            = null
    }
  ]

  admin_user = {
    username = "crayonadm"
    ssh_key  = file("~/.ssh/id_rsa.pub")
  }

  depends_on = [azurerm_subnet.server]
  tags       = local.tags
}