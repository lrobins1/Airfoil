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

import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import pandas as pd



server = Flask(__name__)
app = dash.Dash(server=server)


def make_celery(server):
    celery = Celery(server.name,backend='rpc://', broker='amqp://guest@127.0.0.1:5672')
    celery.conf.update(server.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with server.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


app.server.config.update(
    CELERY_BROKER_URL='ramqp://guest@127.0.0.1:5672',
    CELERY_RESULT_BACKEND='rpc://',
)
celery = make_celery(app.server)

@celery.task()
def launch_analyse(param1,param2,param3,param4): #launch the analyse of 1 file with the given arguments
    data=subprocess.check_output(['./airfoil', param1, param2, param3, param4,'./murtazo/cloudnaca/msh/r2a15n200.xml'])

num_lines = sum(1 for line in open('results/drag_ligt.m'))
with open('results/drag_ligt.m') as rawFile:
    lines = rawFile.readlines()
with open("drag_lift.csv", 'w+') as rawFile:
    for number, line in enumerate(lines):
        if number not in [1, 2, num_lines, num_lines-1, num_lines-2]:
            line = line.lstrip('%%')
            line = line.replace(' ', '')
            line = line.replace('\t', ',')
            rawFile.write(line)

with open ("drag_lift.csv", "r") as result:
    df = pd.read_csv(result)
    global figLine
    figLine = px.line(df, x="drag", y="lift", title='Lift Drag Figure')

app.layout = html.Div(children=[
    html.H1(children='Airfoil'),
    html.Div(children='''
    Airfoil lift vs. drag result.
    '''),
    dcc.Graph(
        id='test-fig',
        figure=figLine
    )
]) 

@server.route('/analyse', methods=['GET'])
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
    app.run_server(host='0.0.0.0', port=8050, debug=True)
