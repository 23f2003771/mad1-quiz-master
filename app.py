from flask import Flask
from controllers.models import db

app = None

def start_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Quiz_Master.db'
    db.init_app(app)
    app.app_context().push()
    app.debug=True

start_app()

from controllers.controllers import *

if __name__ == '__main__':
    app.run()