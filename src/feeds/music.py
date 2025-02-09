from src.feeds.feeddata import FeedData
from src.db.database import Post

def filter(author : str, record : dict) -> bool :
    lower_text : str = record['text'].lower()
    return ((not 'reply' in record) and ('music' in lower_text))

def get_posts() :
    return Post.select().where(Post.feed == 'music')

feed = FeedData('music', filter, get_posts)