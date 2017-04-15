from sqlalchemy import Table, Column, DateTime, BigInteger, Boolean, DateTime, Text
from sqlalchemy.orm import mapper
from sqlalchemy.dialects.sqlite.base import BOOLEAN
from database import metadata, db_session

class Prospect(object):
    query = db_session.query_property()

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

prospect_table = Table('prospect', metadata,
    Column('id', Text, primary_key=True),
    Column('img_url', Text, nullable=False),
    Column('screen_name', Text, nullable=False),
    Column('name', Text, nullable=False),
    Column('created_at', DateTime, nullable=False), ## put it in local time
    Column('description', Text, nullable=False),
    Column('tweet_count', BigInteger, nullable=False),
    Column('favorite_count', BigInteger, nullable=False),
    Column('follower_count', Text, nullable=False),
    Column('following_count', BigInteger, nullable=False),
    Column('verified', Boolean, nullable=False),
    Column('protected', Boolean, nullable=False),
    Column('utc_offset', BigInteger, nullable=False),
)

mapper(Prospect, prospect_table)

# class Tweet(object):
#     query = db_session.query_property()
