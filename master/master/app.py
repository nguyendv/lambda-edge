import random
from flask import Flask, send_file
from flask import jsonify, request
from peewee import Model, SqliteDatabase
from peewee import CharField, IPField
from peewee import IntegrityError

from pathlib import Path 

db = SqliteDatabase('master.db')

class Function(Model):
    path = CharField()
    class Meta:
        database = db

class Worker(Model):
    ip = IPField(unique=True)
    class Meta:
        database = db

db.connect()
db.create_tables([Function,Worker])

app = Flask(__name__)

@app.route('/connections/', methods = ['POST'])
def post_connection():
    return jsonify(message='ok')

@app.route('/workers/', methods = ['POST'])
def post_worker():
    ip = request.remote_addr
    new_worker = Worker(ip=ip)
    try:
        new_worker.save()
    except IntegrityError:
        pass
    return jsonify(message='ok')

@app.route('/functions/', methods = ['POST'])
def post_function():
    f = request.files['upload']
    path = 'functions/' + f.filename

    new_func = Function(path=path)
    new_func.save()
    f.save(path)
    return jsonify(id=new_func.id)

@app.route('/functions/<id>', methods=['GET'])
def get_function(id):
    func = Function.get_by_id(id)
    path = Path(func.path)
    return jsonify(fname=path.name)

@app.route('/clients/', methods=['POST'])
def post_client():
    worker_ips = [worker.ip for worker in Worker.select()]
    return jsonify(gateway=random.choice(worker_ips))


@app.route('/download/<fname>', methods=['GET'])
def download(fname):
    return send_file('functions/' + fname, as_attachment=True)
