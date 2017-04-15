from application_only_auth import Client, ClientException
from models import Prospect
from database import db_session
import urllib, json

CONSUMER_KEY = 	"c9MrxfE3ohZIB5xaXUtCEkuzZ"
CONSUMER_SECRET = "lv3mTkTGkIrVMQGwxiGxGWzGFtvOLy8RrJ8IBIgkyug5JZO6OX"

USER_ENDPOINT = "https://api.twitter.com/1.1/users/lookup.json?"
TWEET_ENDPOINT = "https://api.twitter.com/1.1/statuses/user_timeline.json?"
FRIEND_ENDPOINT = "https://api.twitter.com/1.1/friends/ids.json?"

client = Client(CONSUMER_KEY, CONSUMER_SECRET)

def add_prospect(handle):
    payload = {"screen_name": handle}
    url = "{}{}".format(USER_ENDPOINT, urllib.urlencode(payload))
    response = client.request(url)
    user = response[0]

    prospect = Prospect(
        id=user['id_str'],
        img_url=user['profile_image_url_https'],
        screen_name=user['screen_name'],
        name=user['name'],
        created_at=user['created_at'],
        description=user['description'],
        tweet_count=user['statuses_count'],
        favorite_count=user['favourites_count'],
        follower_count=user['followers_count'],
        following_count=user['friends_count'],
        verified=user['verified'],
        protected=user['protected'],
        utc_offset=user['utc_offset'],
    )

    db_session.merge(prospect)
    commit()

def commit():
    db_session.commit()
    # try:
    #     session.commit()
    # except SQLAlchemyError as e:
    #     session.rollback()
    #     print (str(e))
