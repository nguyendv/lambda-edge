from flask import Flask, request, jsonify
from peewee import SqliteDatabase, Model
from peewee import IntegerField, CharField
from peewee import DoesNotExist
import docker

from pathlib import Path
import requests
import config

docker_client = docker.from_env()

db = SqliteDatabase('worker.db')

class Task(Model):
    func_id = IntegerField()
    status = CharField()
    class Meta:
        database = db

class Function(Model):
    path = CharField()
    class Meta:
        database = db

db.connect()
db.create_tables([Task, Function])

app = Flask(__name__)

IMAGE = "nguyendv/image2license"

@app.route('/tasks/', methods=['POST'])
def post_task():
    func_id = request.get_json()['id']
    argv = request.get_json()['argv']

    # download function if not exists
    try:
        f = Function.get_by_id(func_id)
    except DoesNotExist:
        host = config.get('MASTER_HOST')
        print(host)
        r = requests.get(host + '/functions/' + str(func_id))
        if r.status_code != 200:
            print("Error downloading function from master")
            return jsonify(error="error"), 400
        
        fname = r.json()['fname']
        r = requests.get(host + '/download/' + fname, stream=True)

        with open('data/functions/' + fname, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

    data_path = Path('data')
    print(data_path.absolute())
    try:
        container = docker_client.containers.get('container')
    except docker.errors.NotFound:
        container = docker_client.containers.run(IMAGE, argv, 
                volumes = {data_path.absolute(): {'bind': '/data', 'mode': 'ro'}}, 
                detach=True, 
                name="container", 
                restart_policy = {'Name': 'always'}
        )
        

    cmd = ["python3", "/data/functions/" + fname] + argv
    ret = container.exec_run(cmd=cmd)
    return jsonify(ret=str(ret.output))


@app.route('/tasks/<id>', methods=['GET'])
def get_task(id):
    t = Task.get_by_id(id)
    return jsonify(status=t.status, result=t.result)


@app.route('/upload/<filename>', methods=['POST'])
def upload(filename):
    f = request.files['upload_file']
    f.save('data/upload/' + filename )
    return "ok"

def _execute_func():
    pass
    
