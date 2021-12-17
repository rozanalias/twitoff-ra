import numpy as np
from sklearn.linear_model import LogisticRegression
from .models import User, DB, Tweet
from .twitter import vectorize_tweet, user_tweets


def predict_user(user0_username, user1_username, hypo_tweet_text):
    '''
    Detmerine and predict which user is more likely to say a givUn tweet
    '''
    # Query the data base for user
    user0 = User.query.filter(User.username == user0_username).one()
    user1 = User.query.filter(User.username == user1_username).one()
    
    # Get a list of word embeddings for user's tweets 
    user0_vect = np.array([tweet.vect for tweet in user0.tweets])
    user1_vect = np.array([tweet.vect for tweet in user1.tweets])


    # combine the users's word embeddings into np aray 
    vects = np.vstack([user0_vect, user1_vect])
    zeros = np.zeros(len(user0.tweets))
    ones = np.ones(len(user1.tweets))

    # y vector for training
    labels = np.concatenate([zeros, ones])

    #train to LG
    lg = LogisticRegression()
    lg.fit(vects, labels)

    #generate prediction 
    # vectorize my hypo tweet text
    hypo_tweet_vect = vectorize_tweet(hypo_tweet_text)
    
    #pass 2-dim numpy array to predict
    pred = lg.predict([hypo_tweet_vect])
    return pred[0]

#predict_user('nycdmv', 'nasa', 'will also be important for mars')
