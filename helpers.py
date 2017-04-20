from sqlalchemy import func
from models import Tweet, Prospect
from database import db_session

def get_tweets_by_hour(prospect_id):
    utc_offset = int(Prospect.query.with_entities(Prospect.utc_offset).filter_by(id=prospect_id).one()[0])
    # Create array to store hourly data
    data = [None] * 24
    results = db_session.query(func.count(Tweet.id).label('Count'), func.extract('hour', Tweet.created_at).label('Hour')).filter_by(prospect_id=prospect_id).group_by('Hour').all()
    for pair in results:
        hour = shift_by_timezone(int(pair[1]), utc_offset)
        data[hour] = int(pair[0])
    print data
    return data

def shift_by_timezone(hour, utc_offset):
    shift = utc_offset / 3600
    result = hour + shift
    if result < 0:
        result += 24
    return result % 24
