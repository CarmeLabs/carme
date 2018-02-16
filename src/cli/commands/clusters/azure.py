def azure_commands(self):
    """This functions creates a variety of commands to augment the configuration of Kubernetes on the Google cloud platform.
    """
    lc=self.launch_config
    commands={}
    commands['login']="az login"
    commands['login_sa']="echo 'Service account login not yet available for Azure'"
    commands['create_project']="az group create --name "+lc['a_resource_group']+ " --location "+ lc['a_location']
    commands['set_project']="echo 'No need to set project in Azure.'"
    commands['set_zone']="echo 'No need to set project in Azure.'"
    commands['delete_project']="az group delete --name "+lc['a_resource_group']+" --yes"
    commands['list-locations']="az account list-locations"
    commands['autoscale']="echo 'Autoscaling currently not possible.'"
    commands['create_sp']="az ad sp create-for-rbac --role=Contributor --scopes=/subscriptions/${SUBSCRIPTION_ID} > sp.json"
    if lc['a_service_type']=="aks":
        commands['create']="az aks create --name "+lc['a_cluster_name']+" ---resource-group "+lc['a_resource_group'] +" --location "+lc['a_location']+" --node-count "+str(lc['a_num_nodes'])+" --node-vm-size "+lc['a_machine_type']+" --generate-ssh-keys"
        commands['describe']="az aks list --resource-group "+lc['a_resource_group']
        commands['delete']="az aks delete --name "+lc['a_cluster_name']+" --resource-group "+lc['a_resource_group']
        commands['get_credentials']="az aks get-credentials --resource-group "+lc['a_resource_group']+" --name "+lc['a_cluster_name']
        commands['normal_size']="az aks scale  --node-count "+str(lc['a_num_nodes']) +" --name "+lc['a_cluster_name']+" --resource-group "+lc['a_resource_group']
        commands['class_size']="az aks scale --node-count "+ str(lc['a_num_nodes_class'])+" --name "+lc['a_cluster_name']+" --resource-group "+lc['a_resource_group']
    elif lc['a_service_type']=="acs":
        commands['create']="az acs create --orchestrator-type=kubernetes --resource-group="+lc['a_resource_group'] +" --name="+lc['a_cluster_name']+" --dns-prefix="+lc['a_dns_prefix']+" --node-count="+str(lc['a_num_nodes'])+" --node-vm-size="+lc['a_machine_type']+" --generate-ssh-keys"
        commands['describe']="az acs list  --resource-group="+lc['a_resource_group']
        commands['delete']="az acs delete  --resource-group="+lc['a_resource_group']+" --name="+lc['a_cluster_name']
        commands['get_credentials']="az acs kubernetes get-credentials --resource-group="+lc['a_resource_group']+" --name="+lc['a_cluster_name']#+" --ssh-key-file=~/.ssh/id_rsa_"+lc['a_cluster_name']
        commands['normal_size']="az acs scale --resource-group="+lc['a_resource_group']+" --name="+lc['a_cluster_name']+" --new-agent-count "+str(lc['a_num_nodes'])
        commands['class_size']="az acs scale --resource-group="+lc['a_resource_group']+" --name="+lc['a_cluster_name']+" --new-agent-count "+str(lc['a_num_nodes_class'])
    commands['install_helm']='helm init --client-only'
    # Can't size to 0 lc['a_stop_cluster']="az acs scale --resource-group="+lc['a_resource_group']+" --name="+lc['a_cluster_name']+" --new-agent-count 0"
    commands['create_storage']= "az storage account create --resource-group="+lc['a_resource_group']+" --location="+lc['a_location']+" --sku=Standard_LRS  --name="+lc['a_storage_account']+" --kind=Storage"
    commands['get_storage_key']="az storage account keys list --account-name="+lc['a_storage_account']+" --resource-group="+lc['a_resource_group']+" --output=json | jq .[0].value -r"
    commands['create_keyvault']="az keyvault create --name="+lc['a_cluster_name']+" --resource-group="+ lc['a_resource_group']+" --location="+lc['a_location']+" --enabled-for-template-deployment true"
    commands['backup_private_key']="az keyvault secret set --vault-name="+ lc['a_cluster_name']+ " --name=id-rsa-"+lc['a_cluster_name']+" --file=~/.ssh/id_rsa_"+lc['a_cluster_name']
    commands['backup_public_key']="az keyvault secret set --vault-name="+ lc['a_cluster_name']+ " --name=id-rsa"+lc['a_cluster_name']+"-pub --file=~/.ssh/id_rsa_"+lc['a_cluster_name']+".pub"
    commands['get_private_key']="az keyvault secret show --vault-name="+ lc['a_cluster_name']+ " --name=id-rsa-"+lc['a_cluster_name']
    commands['get_public_key']="az keyvault secret show --vault-name="+ lc['a_cluster_name']+ " --name=id-rsa"+lc['a_cluster_name']+"-pub"
    return commands
