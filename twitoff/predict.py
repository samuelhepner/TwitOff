"""Prediction of Users based on Tweet embeddings."""
import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User
from .twitter import BASILICA
from sklearn.ensemble import RandomForestRegressor


def predict_user(user1_name, user2_name, tweet_text):
    """Determine and return which user is more likely to say a given Tweet."""
    user1 = User.query.filter(User.name == user1_name).one()
    user2 = User.query.filter(User.name == user2_name).one()
    user1_embeddings = np.array([tweet.embedding for tweet in user1.tweets])
    user2_embeddings = np.array([tweet.embedding for tweet in user2.tweets])
    embeddings = np.vstack([user1_embeddings, user2_embeddings])
    labels = np.concatenate([np.ones(len(user1.tweets)),
                             np.zeros(len(user2.tweets))])
    log_reg = LogisticRegression(solver='lbfgs', max_iter=1000).fit(
                                                                    embeddings,
                                                                    labels)

    # forest_reg = RandomForestRegressor(n_estimators=100, max_depth=3,
    #                                    n_jobs=-1, random_state=42).fit(
    #                                                                 embeddings,
    #                                                                 labels)

    tweet_embedding = BASILICA.embed_sentence(tweet_text, model='twitter')
    return log_reg.predict_proba(np.array([tweet_embedding]))[:, 1]
    # return forest_reg.predict(np.array([tweet_embedding]).reshape(1, -1))
