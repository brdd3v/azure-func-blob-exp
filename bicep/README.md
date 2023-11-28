## NOTES


`
bicep build main.bicep
`

`
az deployment sub create --location germanywestcentral --template-file main.json
`

`
zip -jr ../code.zip ../code
`

`
az functionapp deployment source config-zip -g resource-group-exp -n linux-function-app-exp --build-remote true --src ../code.zip
`

