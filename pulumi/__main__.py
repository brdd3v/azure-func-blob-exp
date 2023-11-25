"""An Azure Python Pulumi program"""

import pulumi_archive as archive
from pulumi_azure import core, storage, appservice


resource_group = core.ResourceGroup('resource_group',
                                    name='resource-group-exp',
                                    location='Germany West Central')

account = storage.Account('storage_account',
                          name="saccount01exp",
                          resource_group_name=resource_group.name,
                          location=resource_group.location,
                          account_tier="Standard",
                          account_replication_type='LRS')

container = storage.Container('container',
                              name='container-exp',
                              storage_account_name=account.name)

service_plan = appservice.ServicePlan('service_plan',
                                      name='service-plan-exp',
                                      resource_group_name=resource_group.name,
                                      location=resource_group.location,
                                      os_type='Linux',
                                      sku_name='B1')

appservice.LinuxFunctionApp('linux_function',
                            name='linux-function-app-exp',
                            resource_group_name=resource_group.name,
                            location=resource_group.location,
                            service_plan_id=service_plan.id,

                            storage_account_name=account.name,
                            storage_account_access_key=account.primary_access_key,

                            zip_deploy_file=archive.File("archive",
                                                         type="zip",
                                                         source_dir="../code",
                                                         output_path="../code.zip").output_path,

                            site_config=appservice.LinuxFunctionAppSiteConfigArgs(
                                application_stack=appservice.LinuxFunctionAppSiteConfigApplicationStackArgs(
                                    python_version='3.10'
                                )
                            ),
                            app_settings={
                                'SCM_DO_BUILD_DURING_DEPLOYMENT': True,
                                'FUNCTIONS_WORKER_RUNTIME': 'python'
                            })
