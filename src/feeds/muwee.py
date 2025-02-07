from src.feeds.feeddata import FeedData
from src.db.database import Post

MUWEE_DID : str = 'did:plc:f3mkgbj4ibmtmn2u4b2dpgid'

def filter(author : str, record : dict) -> bool :
    lower_text : str = record['text'].lower()
    return ((not 'reply' in record) and 
            (('#muwee' in lower_text)
             or ('@musicweeklies.bsky.social' in lower_text)
             or author == MUWEE_DID))

def get_posts() :
    return Post.select().where(Post.feed == 'muwee-posts')

feed = FeedData('muwee-posts', filter, get_posts)