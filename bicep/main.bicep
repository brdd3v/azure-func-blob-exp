// main.bicep

targetScope = 'subscription'

param location string = 'germanywestcentral'

resource resourceGroup 'Microsoft.Resources/resourceGroups@2023-07-01' = {
  name: 'resource-group-exp'
  location: location
}

module resources 'resources.bicep' = {
  name: 'resources'
  scope: resourceGroup
  params: {
    location: location
  }
}
