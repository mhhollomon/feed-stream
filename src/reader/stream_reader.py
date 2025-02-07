import websocket
import json
import logging
import rel

from src.feeds import FEEDS
from src.utils import at_post_uri

from datetime import datetime

WRITE_INTERVAL = 5 # seconds

from src.db.database import db, Post

logger = logging.getLogger(__name__)

WEBSOCKET_ADDR : str = "wss://jetstream2.us-east.bsky.network/subscribe?wantedCollections=app.bsky.feed.post"

CREATED : list[dict] = []
DELETED : list = []

def sweep_to_db() -> bool :
    logger.debug("------------- Starting DB writes")
    logger.debug("---- deleting records")
    with db.atomic() :
        Post.delete().where(Post.uri.in_(DELETED)) # type: ignore
        logger.debug(f"Deleted {len(DELETED)} records")
    DELETED.clear()

    logger.debug("---- writing records")
    if len(CREATED) > 0 :
        with db.atomic() :
            Post.insert_many(CREATED).execute()
        logger.debug(f"Wrote {len(CREATED)} records")
        CREATED.clear()
    else :
        logger.debug(f"Nothing to do")

    return True

def on_message(ws, message):

    msg_obj = json.loads(message)
    author = msg_obj['did']

    if ('commit' in msg_obj) :
        data = msg_obj['commit']

        collection = data['collection']
        rkey = data['rkey']
        if data['operation'] == "create" :
            record = data['record']
            cid = data['cid']
            create_date = record['createdAt']

            for feed in FEEDS :
                if feed.filter(author, record) :
                    uri = at_post_uri(author, collection, rkey)
                    logger.debug(f"{feed.shortname} uri = {uri}")
                    create_dict = {'uri' : uri,
                                   'cid' : cid,
                                   'author' : author,
                                   'feed' : feed.shortname,
                                   'indexed_at' : datetime.fromisoformat(create_date)
                                   }
                    CREATED.append(create_dict)

        elif data['operation'] == "delete" :
            rkey = data['rkey']
            #logger.debug('-- delete msg  = ' + message)
            DELETED.append(at_post_uri(author, collection, rkey))
    

def on_error(ws, error):
    logger.error(error)

def on_close(ws, close_status_code, close_msg):
    logger.info("### closed ###")

def on_open(ws):
    logger.info("Opened connection")

def create_websocket() -> websocket.WebSocketApp :
    ws = websocket.WebSocketApp(WEBSOCKET_ADDR,
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)
    
    return ws

def create_periodic() -> None :
    rel.timeout(WRITE_INTERVAL, sweep_to_db )

