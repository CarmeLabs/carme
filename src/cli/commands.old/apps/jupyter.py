import ruamel.yaml
import sys
def jupyterhub_commands(self):
    lc=self.launch_config
    commands={}
    lc['jup_instance']=self.cwd+"/jupyter/"+lc['jup_namespace']
    lc['jup_config']=self.cwd+"/jupyter/"+lc['jup_namespace']+"/config.yaml"
    lc['jup_base']=self.cwd+"/jupyter/"+lc['jup_namespace']+"/values.yaml"
    #commands['install_ssl']="helm install --name=letsencrypt --namespace=kube-system stable/kube-lego --set config.LEGO_EMAIL="+lc['jup_email']+" --set config.LEGO_URL=https://acme-v01.api.letsencrypt.org/directory"
    commands['init']="This will do multiple steps to initialze Jupyter config."
    commands['show_config']="cat "+lc['jup_config']
    commands['clone_repo']="helm repo add jupyterhub "+lc['jup_helm_repo']+" && helm repo update"
    commands['install']="helm install jupyterhub/jupyterhub --version="+lc['jup_version']+" --name="+lc['jup_releasename']+" --namespace="+lc['jup_namespace']+" -f "+lc['jup_config']
    commands['upgrade']="helm upgrade "+lc['jup_namespace']+" jupyterhub/jupyterhub --version="+lc['jup_version']+" -f "+lc['jup_config']
    commands['describe']="kubectl --namespace="+lc['jup_namespace']+" get pod"
    commands['get_ip']="kubectl --namespace="+ lc['jup_namespace']+" get svc proxy-public"
    commands['delete_namespace']="kubectl delete namespace "+lc['jup_namespace']
    commands['delete']="helm delete "+lc['jup_releasename']+" --purge"
    commands['delete_namespace']="kubectl delete namespace "+lc['jup_namespace']
    #if lc['jup_ssl']:
    #    lc['jup_callback_url']= "https://"
    #else:
#        lc['jup_callback_url']= "http://"
#    lc['jup_callback_url']=lc['jup_callback_url']+lc['jup_url']+"/hub/oauth_callback"
    commands['jup_get_logs']="kubectl --namespace="+lc['jup_namespace']+" logs <insert_podname>"
    return commands

def jupyter_action(self):
    self.check_launch_file('jup_namespace')
    self.app_commands=jupyterhub_commands(self)
    if self.options['<command>']=='list':
        print("Listing out available commands.")
        print(ruamel.yaml.dump(self.app_commands, sys.stdout, Dumper=ruamel.yaml.RoundTripDumper))
    elif self.options['<command>']=='init':
        jupyter_init(self)
    elif self.options['<command>'][:4]=='jup_':
        if self.options['<command>'] in self.launch_config:
            print("setting config for ", self.options['<command>'])
            update_config(self,self.options['<command>'])
        else:
            print("Configuration ", self.options['<command>'], " was not found in the launchfile." )
    elif self.options['<command>'] in self.app_commands:
        #bash_command(self.options['<command>'], self.app_commands[self.options['<command>']], dry-run=False)
        print(self.bash_command(self.options['<command>'],self.app_commands[self.options['<command>']]))
    else:
        print("That command isn't available yet. Use `carme app "+self.options['<command>']+" list` to see available commands.")
    return

def update_config(self, key):
    file=self.cwd+"/jupyter/"+self.launch_config['jup_namespace']+"/config.yaml"
    config = ruamel.yaml.round_trip_load(open(file), preserve_quotes=True)
    if key[4:] in config:
        print("updating config")
        config[key[4:]]=self.launch_config[key]
    else:
        print("inserting config")
        config.insert(len(config), key[4:], self.launch_config[key])
    ruamel.yaml.round_trip_dump(config, open(file, 'w'))
    return

def jupyter_init(self):
    lc=self.launch_config
    lc['jup_instance']=self.cwd+"/jupyter/"+lc['jup_namespace']
    lc['jup_config']=self.cwd+"/jupyter/"+lc['jup_namespace']+"/config.yaml"
    #lc['jup_base']=self.cwd+"/jupyter/"+lc['jup_namespace']+"/values.yaml"
    if lc['jup_rebuild_config']:
        print(self.bash_command('delete folder','rm -rf '+lc['jup_instance']))
        print(self.bash_command('create directory', 'mkdir jupyter'))
        print(self.bash_command('create directory', 'mkdir '+ lc['jup_instance']))
        #Random variable that will be added to the config file.
        self.bash_command("generate secret key", "openssl rand -hex 32 > "+ lc['jup_instance']+"/cookie_secret.txt")
        #Random variable that will be added to the config file.
        self.bash_command("generate secret token", "openssl rand -hex 32 > "+ lc['jup_instance']+"/secret_token.txt")
    #     #download reference config
        self.bash_command("get reference config", "wget -P "+ lc['jup_instance']+" "+lc['jup_config_init'])
        self.bash_command("move reference config","mv "+ lc['jup_instance']+"/values.yaml " +lc['jup_instance']+"/reference.yaml")
         #init_jupyterhub_config(lc)
        if lc['jup_set_fixed_ip']:
            inp = """    #These are the only two required fields we need to launch
             proxy:
               secretToken: null
               service:
                  loadBalancerIP: null
             hub:
                   cookieSecret: null
                 """
        else:
             inp = """    #These are the only two required fields we need to launch
             proxy:
               secretToken: null
             hub:
               cookieSecret: null
                 """
    #         #This will write out a basic .YAML file.
        with open(lc['jup_instance']+'/cookie_secret.txt', 'r') as f:
                   cookie_secret = f.read().rstrip()
        with open(lc['jup_instance']+'/secret_token.txt', 'r') as f:
                   secret_token = f.read().rstrip()
    #
        config = ruamel.yaml.load(inp, ruamel.yaml.RoundTripLoader)

        config['hub']['cookieSecret']=cookie_secret
        config['proxy']['secretToken']=secret_token
        if lc['jup_set_fixed_ip']:
            config['proxy']['service']['loadBalancerIP']=lc['jup_fixed_ip']
        if lc['cluster_location']=='azure':
            config['prePuller']=lc['jup_prePuller']
            config['rbac']=lc['jup_prePuller']
            print("RBAC set to false per https://github.com/jupyterhub/zero-to-jupyterhub-k8s/issues/344. This is a security issue. Check for updates.")
        ruamel.yaml.round_trip_dump(config, open(lc['jup_config'], 'w'))
        lc['jup_rebuild_config']=False
        ruamel.yaml.round_trip_dump(lc, open(self.launch_file, 'w'))
    else:
        print("Currently the launchfile 'jup_rebuild_config' parameter is set to false.")
    return
