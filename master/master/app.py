from flask import Flask
from flask import jsonify

app = Flask(__name__)

@app.route('/connections', methods = ['POST'])
def post_connection():
    return jsonify(message='ok')
