import base64
import os

from flask import Flask, redirect, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine


app = Flask(__name__)
connection = None

def establish_conn():
    global connection
    engine = create_engine('mysql+mysqldb://root:abcdxyz@abcdxyz/TECHBUDDY_DB')
    connection = engine.connect()

def query(query_string):
    result = connection.execute(query_string)
    return result

@app.route('/')
def homepage():
    establish_conn()
    query_string = 'select * from Persons;'
    response = query(query_string)
    print("RESPONSE: "),
    for res in response:
        print(res)
    return render_template('homepage.html')

@app.route('/requests', methods=['GET','POST'])
def handleRequests():
    if request.method == 'GET':
        print('get request received')
        return jsonify({'request': request.args.get('query'), 'value':request.args.get('val')})
    elif request.method == 'POST':
        print('post request received')
    else:
        print('unidentified request')

@app.errorhandler(500)
def server_error(e):
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


if __name__ == '__main__':
    print('main.py called')
    app.run(host='127.0.0.1', port=8080, debug=True)
