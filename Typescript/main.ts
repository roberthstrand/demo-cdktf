import { Construct } from "constructs";
import { App, TerraformStack, Token } from "cdktf";
import { CrayonVmAzurerm } from "./.gen/modules/crayon/vm/azurerm";
import {
  AzurermProvider,
  ResourceGroup,
  VirtualNetwork,
  Subnet
} from "./.gen/providers/azurerm";

class MyStack extends TerraformStack {
  constructor(scope: Construct, name: string) {
    super(scope, name);

    new AzurermProvider(this, 'azureFeature', {
      features: [{}],
    });

    const location = "Norway East"
    const tags = {
      "environment": "demo",
      "source": "cdktf",
      "lang": "typescript"
    }

    const serverRg = new ResourceGroup(this, 'server_rg', {
      name: 'cdktf-rg',
      location: location,
      tags: tags
    })

    const serverVnet = new VirtualNetwork(this, 'server_vnet', {
      name: 'cdktf-vnet',
      location: location,
      resourceGroupName: serverRg.name,
      addressSpace: ['10.0.0.0/16'],
      tags: tags
    })

    const serverVnetSubnet = new Subnet(this, 'subnet1', {
      name: 'subnet1',
      resourceGroupName: serverRg.name,
      virtualNetworkName: serverVnet.name,
      addressPrefixes: ['10.0.0.0/24']
    })

    new CrayonVmAzurerm(this, 'server01', {
      name: 'server01',
      resourceGroup: serverRg.name,
      location: location,

      adminUser: {
        username: 'crayonadmin',
        password: 'Pl43s3D0nth4xm3!'
      },
      
      networkInterfaceSubnets: [{
        name: serverVnetSubnet.name,
        virtual_network_name: serverVnet.name,
        resource_group_name: serverRg.name,
        public_ip_id: Token.asAny(null),
        static_ip: Token.asAny(null)
      }],

      tags: tags
    })
  }
}

const app = new App();
new MyStack(app, "Typescript");
app.synth();
