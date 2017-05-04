import urllib, json
from application_only_auth import Client, ClientException

CONSUMER_KEY = 	"c9MrxfE3ohZIB5xaXUtCEkuzZ"
CONSUMER_SECRET = "lv3mTkTGkIrVMQGwxiGxGWzGFtvOLy8RrJ8IBIgkyug5JZO6OX"

USER_ENDPOINT = "https://api.twitter.com/1.1/users/lookup.json?"
TWEET_ENDPOINT = "https://api.twitter.com/1.1/statuses/user_timeline.json?"
FRIEND_ENDPOINT = "https://api.twitter.com/1.1/friends/ids.json?"

client = Client(CONSUMER_KEY, CONSUMER_SECRET)

def add_prospect(handle):
    from app import db
    from models import Prospect
    prospect = Prospect.query.filter_by(screen_name=handle).first()
    if prospect is None:
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
        db.session.merge(prospect)
        db.session.commit()
    return prospect.id

def get_tweets(prospect_id):
    from app import db
    from models import Prospect
    tweet_id = None
    # Begin collecting tweets 200/req up to 3200 tweets
    for batch in range(0, 16):
        tweet_id = add_tweet_batch(prospect_id, tweet_id)
        if tweet_id == 0:
            break
    Prospect.query.filter_by(id=prospect_id).update(dict(has_tweets=True))
    db.session.commit()

def add_tweet_batch(prospect_id, max_id=None):
    # Create payload
    if max_id == None:
        payload = {"user_id": prospect_id, "count": 200, "include_rts": 1}
    else:
        payload = {"user_id": prospect_id, "max_id": max_id - 1, "count": 200, "include_rts": 1}
    # Build URL
    url = "{}{}".format(TWEET_ENDPOINT, urllib.urlencode(payload))
    # Make requests and retry if RATE LIMIT reached
    print url
    tweets = client.request(url)
    if len(tweets) == 0:
        return 0

    # Save the tweets
    for tweet in tweets:
        add_tweet(tweet, prospect_id)
        add_hashtags(tweet, prospect_id)
        add_urls(tweet, prospect_id)
        add_media(tweet, prospect_id)
        add_user_mentions(tweet, prospect_id)
    return tweets[-1]["id"]

def add_tweet(tweet, prospect_id):
    from app import db
    from models import Tweet
    if 'retweeted_status' in tweet:
        retweet = True
        favorite_count = tweet['retweeted_status']['favorite_count']
    else:
        retweet = False
        favorite_count = tweet['favorite_count']
    country = None
    city = None
    if 'place' in tweet:
        if tweet['place']:
            country = tweet['place']['country']
            city = tweet['place']['full_name']
    t = Tweet(
        id=tweet['id_str'],
        prospect_id=prospect_id,
        body=tweet['text'],
        created_at=tweet['created_at'],
        favorite_count=favorite_count,
        retweet_count=tweet['retweet_count'],
        retweet=retweet,
        country_location=country,
        city_location=city
    )
    db.session.merge(t)

def add_hashtags(tweet, prospect_id):
    from app import db
    from models import Hashtag
    for hashtag_list in tweet['entities']['hashtags']:
        if len(hashtag_list) > 0:
            hashtag = hashtag_list["text"]
            h = Hashtag(
                tweet_id=tweet['id_str'],
                prospect_id=prospect_id,
                hashtag=hashtag
            )
            db.session.merge(h)

def add_urls(tweet, prospect_id):
    from app import db
    from models import URL
    for url_list in tweet['entities']['urls']:
        if len(url_list) > 0:
            url = url_list['display_url']
            u = URL(
                tweet_id=tweet['id_str'],
                prospect_id=prospect_id,
                url=url
            )
            db.session.merge(u)

def add_media(tweet, prospect_id):
    from app import db
    from models import Media
    if 'media' in tweet['entities']:
        media_list = tweet['entities']['media']
        for media in media_list:
            url = media['display_url']
            u = Media(
                tweet_id=tweet['id_str'],
                prospect_id=prospect_id,
                url=url
            )
            db.session.merge(u)

def add_user_mentions(tweet, prospect_id):
    from app import db
    from models import UserMention
    for user_mention_list in tweet['entities']['user_mentions']:
        if len(user_mention_list) > 0:
            user_mention = user_mention_list['screen_name']
            um = UserMention(
                tweet_id=tweet['id_str'],
                prospect_id=prospect_id,
                user_mention=user_mention
            )
            db.session.merge(um)
