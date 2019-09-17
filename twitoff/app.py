# My app
from flask import Flask
from .models import db


# make our own app factory
def create_app():
    app = Flask(__name__)

    # add config
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

    # add in database init later
    db.init_app(app)

    # create the route
    @app.route('/')
    # define the function
    def root():
        return 'Welcome to TwitOff!'

    return app
