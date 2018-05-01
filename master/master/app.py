from flask import Flask
from flask import jsonify, request
from peewee import Model, SqliteDatabase, CharField

db = SqliteDatabase('master.db')

class Function(Model):
    path = CharField()
    class Meta:
        database = db

db.connect()
db.create_tables([Function,])

app = Flask(__name__)

@app.route('/connections/', methods = ['POST'])
def post_connection():
    return jsonify(message='ok')

@app.route('/functions/', methods = ['POST'])
def post_function():
    f = request.files['upload']
    path = 'functions/' + f.filename

    new_func = Function(path=path)
    new_func.save()
    f.save(path)
    return jsonify(id=new_func.id)
