from src.feeds.feeddata import FeedData
from datetime import datetime, timezone
from src.db.database import Post

import logging

CURSOR_EOF = 'eof'

logger = logging.getLogger(__name__)

def compute_feed(feed : FeedData, cursor : str|None, limit : int) -> dict :
    retval = {}

    indexed_at : datetime = datetime.now()
    cid : str = ''

    if cursor :
        if cursor == CURSOR_EOF :
            return {
                'cursor': CURSOR_EOF,
                'feed': []
            }
 
        cursor_parts = cursor.split('::')
        if len(cursor_parts) != 2:
            raise ValueError('Malformed cursor')

        indexed_at = datetime.fromtimestamp(float(cursor_parts[0]), timezone.utc)
        cid = cursor_parts[1]

    posts = feed.get_posts()
    if cursor :
        posts = posts.where(((Post.indexed_at == indexed_at) & (Post.cid < cid)) | (Post.indexed_at < indexed_at)) # type: ignore

    posts = posts.order_by(Post.indexed_at.desc(), Post.cid.desc())
    posts = posts.limit(limit)

    feed_data = [{'post' : post.uri} for post in posts]

    new_cursor : str = CURSOR_EOF
    last_post = posts[-1] if posts else None
    if last_post:
        logger.debug(f"last post = {last_post.uri}")
        new_cursor = f'{datetime.fromisoformat(last_post.indexed_at).timestamp()}::{last_post.cid}' 

    return {
        'cursor': new_cursor,
        'feed': feed_data
    }