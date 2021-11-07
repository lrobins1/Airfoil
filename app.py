from celery import Celery
import os
import subprocess
import sys
from os import listdir
from os.path import isfile, join,dirname
import random
import time
import json
from collections import Counter
from flask import Flask, jsonify
import base64


app = Flask(__name__)


#initialize celery
celery = Celery(app.name,backend='rpc://', broker='amqp://group7:group7@130.238.28.111:5672/group7host')

@celery.task
def launch_analyse(param1,param2,param3,param4): #launch the analyse of 1 file with the given arguments
    data=subprocess.check_output(['./airfoil', param1, param2, param3, param4,'./murtazo/cloudnaca/msh/r2a15n200.xml'])
    print(data)
    return data

@app.route('/analyse', methods=['GET'])
def analyse():
    param1 = ['10','5']
    param2 = ['0.0001','0.00005']
    param3 = ['10.','5.']
    param4 = ['1','1']
    datas = []
    results = []

    for n in range(len(param1)):
        data = launch_analyse.delay(param1[n],param2[n],param3[n],param4[n])
        datas.append(data)
		
	
    for n in range(len(datas)):
        data2 = datas[n]
        result = data2.get()
        results.append(result)

    return results


if __name__ == '__main__':

    app.run(host='0.0.0.0',debug=True)
