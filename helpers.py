from sqlalchemy import func, desc
from models import Tweet, Prospect, Hashtag, UserMention, URL
from database import db_session

def get_tweets_by_hour(prospect_id):
    utc_offset = int(Prospect.query.with_entities(Prospect.utc_offset).filter_by(id=prospect_id).one()[0])
    # Create array to store hourly data
    data = [None] * 24
    results = db_session.query(func.count(Tweet.id).label('Count'), func.extract('hour', Tweet.created_at).label('Hour')).filter_by(prospect_id=prospect_id).group_by('Hour').all()
    for pair in results:
        hour = shift_by_timezone(int(pair[1]), utc_offset)
        data[hour] = int(pair[0])
    return data

def shift_by_timezone(hour, utc_offset):
    shift = utc_offset / 3600
    result = hour + shift
    if result < 0:
        result += 24
    return result % 24

def get_most_common_hashtags(prospect_id):
    results = db_session.query(Hashtag.hashtag.label('Hashtag'), func.count(Hashtag.id).label('Count')).filter_by(prospect_id=prospect_id).group_by('Hashtag').order_by(desc('Count')).limit(5).all()
    return results

def get_most_common_handles(prospect_id):
    results = db_session.query(UserMention.user_mention.label('User Mention'), func.count(UserMention.id).label('Count')).filter_by(prospect_id=prospect_id).order_by(desc('Count')).group_by('User Mention').limit(5).all()
    return results

def get_most_common_locations(prospect_id):
    results = db_session.query(Tweet.city_location.label('Location'), Tweet.country_location.label('Country'), func.count(Tweet.id).label('Count')).filter_by(prospect_id=prospect_id).order_by(desc('Count')).group_by('Country', 'Location').limit(5).all()
    return results

def get_most_common_profanities(prospect_id):
    pass

def get_image_urls(prospect_id):
    results = Media.query.with_entities(Media.urls).filter_by(prospect_id=prospect_id).all()
    return results
