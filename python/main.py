#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack, Token
from imports.azurerm import AzurermProvider, ResourceGroup, VirtualNetwork, Subnet, NetworkInterface
from imports.crayon.vm.azurerm import CrayonVmAzurerm

class MyStack(TerraformStack):
  def __init__(self, scope: Construct, ns: str):
    super().__init__(scope, ns)

    location="Norway East"
    tags = {
        "environment": "demo",
        "source": "cdktf",
        "lang": "python"
    }

    AzurermProvider(self, "Azurerm",\
      features=[{}]
      )

    server_rg = ResourceGroup(self, 'server_rg',\
      name = "server-rg",
      location = location,
      tags = tags
      )

    server_vnet = VirtualNetwork(self, 'server_vnet', \
      name = "cdktf-vnet",
      location = location,
      address_space = ["10.0.0.0/16"],
      resource_group_name = server_rg.name,
      tags = tags
      )

    server_vnet_subnet1 = Subnet(self, 'server_vnet_subnet1', \
      name = "subnet1",
      resource_group_name = server_rg.name,
      virtual_network_name = server_vnet.name,
      address_prefixes = ["10.0.0.0/24"]
      )

    vmNic = NetworkInterface(self, 'vmNic', \
      name = "vm-nic",
      location = location,
      resource_group_name = server_rg.name,
      ip_configuration = [{
        'name': "internal",
        'subnetId': server_vnet_subnet1.id,
        'privateIpAddressAllocation': "Dynamic",
        }]
      )

    vmModule = CrayonVmAzurerm(self, 'vm', \
      name = "server01",
      resource_group = server_rg.name,
      location = location,
      network_interface_ids = [vmNic.id],

      admin_user = {
        'username': "crayonadm",
        'password': "Pl43s3D0nth4xm3!"
      },
      #depends_on = [server_vnet_subnet1.fqn],
      tags = tags
      )

app = App()
MyStack(app, "python")

app.synth()
