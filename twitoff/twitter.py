import requests
import ast
import spacy
# Local import
from .models import DB, User, Tweet

nlp = spacy.load('my_model/')

def vectorize_tweet(tweet_text):
    # return the word embedding for a given string of text
    return nlp(tweet_text).vector

def user_tweets(username):
    ''' adds a user and their recent tweets to a database '''
    
    # The link at which we will be making calls
    HEROKU_URL = 'https://lambda-ds-twit-assist.herokuapp.com/user/'

   
    try:
        ''' Use the `literal_eval` method to turn the JSON response into a Python dictionary'''
        # Get the user data
        twitter_user = ast.literal_eval(requests.get(HEROKU_URL + username).text)
        twitter_user_id = twitter_user['twitter_handle']['id']
        username = twitter_user['twitter_handle']['username']
        
        # create a db_user and check if it already exist 
        db_user = (User.query.get(twitter_user_id) or User(id=twitter_user_id, username= username))
        
        # Add to the user to the database
        DB.session.add(db_user)

        # Get the user's tweeets
        tweets = twitter_user['tweets']
        tweets_added = 0

        for tweet in tweets:
            '''pull out the tweets list of tweets
            and Get our vectorization (word embeddings)'''
           
            if Tweet.query.get(tweet['id']):
                break
            else:
                tweet_text = tweet['full_text']
                tweet_vector = vectorize_tweet(tweet_text)

                # Otherwise, add a new Tweet record
                db_tweet = Tweet(id=tweet['id'], text=tweet_text, vect=tweet_vector)
                # Append it to the User instance
                db_user.tweets.append(db_tweet)

                # Add it to the database session
                DB.session.add(db_tweet)
                tweets_added += 1
                DB.session.add(db_tweet)
    except Exception as e:
        print(f"Error Processing {username}: {e}")
        raise e
    else:
        # Save the user and user's tweets that were added to the DB.session
        DB.session.commit()

