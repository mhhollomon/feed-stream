import websocket
import json
import logging

from src.db.database import db, Post

logger = logging.getLogger(__name__)

WEBSOCKET_ADDR : str = "wss://jetstream2.us-east.bsky.network/subscribe?wantedCollections=app.bsky.feed.post"

CREATED : list[dict] = []
DELETED : list = []

def delete_records() -> None :
    logger.debug("---- deleting records")
    with db.atomic() :
        Post.delete().where(Post.uri.in_(DELETED)) # type: ignore
    DELETED.clear()

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
            # don't want replies
            if not 'reply' in record :
                lower_text : str = record['text'].lower()
                if 'music' in lower_text :
                    #logger.debug('create msg  = ' + message)
                    logger.debug(f"created date = {create_date} uri = at://{author}/{collection}/{rkey}")
                    create_dict = {'uri' : f'at://{author}/{collection}/{rkey}',
                                   'cid' : cid,
                                   'author' : author,
                                   'feed' : 'music',
                                   'indexed_at' : create_date
                                   }
                    CREATED.append(create_dict)

        elif data['operation'] == "delete" :
            rkey = data['rkey']
            #logger.debug('-- delete msg  = ' + message)
            DELETED.append(f"at://{author}/{collection}/{rkey}")
    
    if len(DELETED) > 100 :
        delete_records()

    if len(CREATED) > 0 :
        with db.atomic() :
            for post_dict in CREATED :
                Post.create(**post_dict)
        CREATED.clear()


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
