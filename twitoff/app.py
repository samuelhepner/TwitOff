# My app
from flask import Flask, render_template, request, redirect
from .models import DB, User
from decouple import config
from .twitter import add_or_update_user
from .predict import predict_user


# make our own app factory
def create_app():
    app = Flask(__name__)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    # Stop tracking modifications
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['ENV'] = config('ENV')
    # now the database knows about the app
    DB.init_app(app)

    # create the route
    @app.route('/')
    # define the function
    def root():
        users = User.query.all()
        return render_template('base.html', title='Home', users=users)

    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
        users = User.query.all()
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = 'User @{} has been successfully added!'.format(name)
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = 'Error adding @{}: {}'.format(name, e)
            tweets = []
        return redirect("https://twitoff-samh3pn3r.herokuapp.com/")

    @app.route('/compare', methods=['POST'])
    def compare(message=''):
        user1, user2 = sorted([request.values['user1'],
                               request.values['user2']])
        if user1 == user2:
            message = 'I cannot compare a user to themselves.'
        else:
            tweet_text = request.values['tweet_text']
            confidence = int(predict_user(user1, user2, tweet_text) * 100)
            if confidence >= 50:
                message = f"""'{tweet_text}' is more likely to be said by
                {user1}, with {confidence}% confidence."""
            else:
                message = f"""'{tweet_text}' is more likely to be said by {user2},
                            with {100 - confidence}% confidence."""
        return render_template('prediction.html', title='Prediction',
                               message=message)

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='DB Reset!', users=[])

    return app
