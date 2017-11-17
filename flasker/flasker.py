import sqlite3
from flask import Flask,request,session,g,redirect,url_for,abort,\
    render_template,flash
from contextlib import closing

#configuration
DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'kinglee'
USERNAME = 'admin'
PASSWORD ='default'


#create our little application
app=Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

if __name__ == '__main__':
    app.run()









# app = Flask(__name__)
#
#
# @app.route('/')
# def hello_world():
#     return 'Hello World!'
#
#
# if __name__ == '__main__':
#     app.run()
