from celery import Celery
import os
import subprocess
import sys
from os import listdir
from os.path import isfile, join, dirname
import random
import time
import json
from collections import Counter
from flask import Flask, jsonify
import base64
import time
import os
import sys
import inspect
from os import environ as env
from novaclient import client
from keystoneauth1 import loading
from keystoneauth1 import session


app = Flask(__name__)


# initialize celery
celery = Celery(app.name, backend='rpc://',
                broker='amqp://group7:group7@130.238.28.111:5672/group7host')

# launch a worker on a new VM


def launch_worker():
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

    cfg_file_path = os.getcwd()+'/cloud-cfg.txt'
    if os.path.isfile(cfg_file_path):
        userdata = open(cfg_file_path)
    else:
        sys.exit("cloud-cfg.txt is not in current working directory")
    secgroups = ['Louis_security_group']
    name = "Airfoil_Worker"
    instance = nova.servers.create(name=name, key_name="Lab01", access_ip_v4="130.238.28.165",
                                   image=image, flavor=flavor, userdata=userdata, nics=nics, security_groups=secgroups)
    inst_status = instance.status
    time.sleep(10)

    while inst_status == 'BUILD':
        time.sleep(5)
        instance = nova.servers.get(instance.id)
        inst_status = instance.status


@celery.task
# launch the analyse of 1 file with the given arguments
def launch_analyse(file, param1, param2, param3, param4):
    filename = './murtazo/cloudnaca/msh/' + file + '.xml'
    data = subprocess.check_output(
        ['./airfoil', param1, param2, param3, param4, filename])
    with open("results/drag_ligt.m", "r") as result:
        data = result.readlines()
    return json.dumps(data)


@app.route('/new_workers/<nworkers>', methods=['GET'])
def new_workers(nworkers):
    for n in range(int(nworkers)):
        launch_worker()
    return ("Workers successfully started")


@app.route('/analyse/<file>', methods=['GET'])
def analyse(file):
    param1 = ['10', '5', '10', '7', '8', '9', '10', '11', '12', '15']
    param2 = ['0.0001', '0.00005', '0.0002', '0.00015', '0.000075',
              '0.0001', '0.0002', '0.0003', '0.00005', '0.0001']
    param3 = ['10.', '5.', '5.', '10.', '7.', '3.', '15.', '20.', '10.', '10.']
    param4 = ['1', '2', '1', '2', '1', '2', '1', '2', '1', '2']
    datas = []
    results = {}

    for n in range(len(param1)):
        data = launch_analyse.delay(
            file, param1[n], param2[n], param3[n], param4[n])
        datas.append(data)

    for n in range(len(datas)):
        data2 = datas[n]
        result = data2.get()
        results[n] = result

    return results


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
