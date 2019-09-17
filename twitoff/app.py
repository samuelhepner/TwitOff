# My app
from flask import Flask, render_template, request
from .models import DB, User
from decouple import config


# make our own app factory
def create_app():
    app = Flask(__name__)

    # add config
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')

    # Stop tracking modifications
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['ENV'] = config('ENV')

    # now the database knows about the app
    DB.init_app(app)

    # create the route
    @app.route('/')
    # define the function
    def root():
        users = User.query.all()
        return render_template('base.html', title='Home', users=users)

    return app
