# http://docs.openstack.org/developer/python-novaclient/ref/v2/servers.html
import time, os, sys
import inspect
from os import environ as env

from  novaclient import client
from keystoneauth1 import loading
from keystoneauth1 import session

flavor = "ssc.medium"
private_net = "UPPMAX 2021/1-5 Internal IPv4 Network"
floating_ip_pool_name = None
floating_ip = None
snapshot_name = "Airfoil-7"

loader = loading.get_plugin_loader('password')

auth = loader.load_from_options(auth_url=env['OS_AUTH_URL'],
                                username=env['OS_USERNAME'],
                                password=env['OS_PASSWORD'],
                                project_name=env['OS_PROJECT_NAME'],
                                project_domain_name=env['OS_USER_DOMAIN_NAME'],
                                project_id=env['OS_PROJECT_ID'],
                                user_domain_name=env['OS_USER_DOMAIN_NAME'])

sess = session.Session(auth=auth)
nova = client.Client('2.1', session=sess)

image = nova.glance.find_image(snapshot_name)

flavor = nova.flavors.find(name=flavor)

if private_net != None:
    net = nova.neutron.find_network(private_net)
    nics = [{'net-id': net.id}]
else:
    sys.exit("private-net not defined.")

cfg_file_path =  os.getcwd()+'/cloud-cfg.txt'
if os.path.isfile(cfg_file_path):
    userdata = open(cfg_file_path)
else:
    sys.exit("cloud-cfg.txt is not in current working directory")

secgroups = ['Louis_security_group']

name = "Worker-gr7"
instance = nova.servers.create(name=name,key_name="Lab01", access_ip_v4="130.238.28.165", image=image, flavor=flavor, userdata=userdata, nics=nics,security_groups=secgroups)
inst_status = instance.status
time.sleep(10)

while inst_status == 'BUILD':
    time.sleep(5)
    instance = nova.servers.get(instance.id)
    inst_status = instance.status

print "Instance: "+ instance.name +" is in " + inst_status + "state"