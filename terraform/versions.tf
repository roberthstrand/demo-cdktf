terraform {
  required_version = "1.0.6"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "2.76.0"
    }
  }
}
provider "azurerm" {
  features {}
}