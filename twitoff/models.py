from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    # Twitter users that we analyze
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), nullable=False)


class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Unicode(280))
