from app import db
from flask_login import UserMixin
from passlib.apps import custom_app_context as pwd_context

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.Text)

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

class Prospect(db.Model):
    __tablename__ = 'prospect'
    id = db.Column(db.Text, primary_key=True)
    img_url = db.Column(db.Text, nullable=False)
    screen_name = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=False)
    tweet_count = db.Column(db.Integer, nullable=False)
    favorite_count = db.Column(db.Integer, nullable=False)
    follower_count = db.Column(db.Integer, nullable=False)
    following_count = db.Column(db.Integer, nullable=False)
    protected = db.Column(db.Boolean, nullable=False)
    verified = db.Column(db.Boolean, nullable=False)
    utc_offset = db.Column(db.Integer, nullable=False)
    has_tweets = db.Column(db.Boolean, nullable=False)

    def __init__(self, id, img_url, screen_name, name, created_at, description, tweet_count, favorite_count, follower_count, following_count,
        verified, protected, utc_offset):
        self.id = id
        self.img_url = img_url
        self.screen_name = screen_name
        self.name = name
        self.created_at = created_at
        self.description = description
        self.tweet_count = tweet_count
        self.favorite_count = favorite_count
        self.follower_count = follower_count
        self.following_count = following_count
        self.verified = verified
        self.protected = protected
        self.utc_offset = utc_offset
        self.has_tweets = False

class Tweet(db.Model):
    id = db.Column(db.Text, primary_key=True)
    prospect_id = db.Column(db.Text, nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    favorite_count = db.Column(db.Integer, nullable=False)
    retweet_count = db.Column(db.Integer, nullable=False)
    retweet = db.Column(db.Boolean, nullable=False)
    country_location = db.Column(db.Text, nullable=True)
    city_location = db.Column(db.Integer, nullable=True)

    def __init__(self, id, prospect_id, body, created_at, favorite_count, retweet_count, retweet, country_location, city_location):
        self.id = id
        self.prospect_id = prospect_id
        self.body = body
        self.created_at = created_at
        self.favorite_count = favorite_count
        self.retweet_count = retweet_count
        self.retweet = retweet
        self.country_location = country_location
        self.city_location = city_location

class Hashtag(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tweet_id = db.Column(db.Text, nullable=False)
    prospect_id = db.Column(db.Text, nullable=False)
    hashtag = db.Column(db.Text, nullable=False)

    def __init__(self, tweet_id, prospect_id, hashtag):
        self.tweet_id = tweet_id
        self.prospect_id = prospect_id
        self.hashtag = hashtag

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tweet_id = db.Column(db.Text, nullable=False)
    prospect_id = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)

    def __init__(self, tweet_id, prospect_id, url):
        self.tweet_id = tweet_id
        self.prospect_id = prospect_id
        self.url = url

class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tweet_id = db.Column(db.Text, nullable=False)
    prospect_id = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)

    def __init__(self, tweet_id, prospect_id, url):
        self.tweet_id = tweet_id
        self.prospect_id = prospect_id
        self.url = url

class UserMention(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tweet_id = db.Column(db.Text, nullable=False)
    prospect_id = db.Column(db.Text, nullable=False)
    user_mention = db.Column(db.Text, nullable=False)

    def __init__(self, tweet_id, prospect_id, user_mention):
        self.tweet_id = tweet_id
        self.prospect_id = prospect_id
        self.user_mention = user_mention
