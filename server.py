import os
from typing import Any, Dict
from flask import Flask, request, abort, jsonify
import src.config as config

from src.utils import at_feed_uri

from src.feeds import FEEDS, find_feed
from src.server.feed_skeleton import compute_feed

import logging

from waitress import serve

logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(name)s:%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def home() :
    abort(404)

@app.route("/ping")
def hello_world():
    return "ping"

@app.get('/.well-known/did.json')
def did_json():
    if not config.SERVICE_DID.endswith(config.HOSTNAME):
        return '', 404

    return jsonify({
        '@context': ['https://www.w3.org/ns/did/v1'],
        'id': config.SERVICE_DID,
        'service': [
            {
                'id': '#bsky_fg',
                'type': 'BskyFeedGenerator',
                'serviceEndpoint': f'https://{config.HOSTNAME}'
            }
        ]
    })

@app.get('/xrpc/app.bsky.feed.describeFeedGenerator')
def describe_feed_generator():
    feeds = [{'uri': at_feed_uri(f.shortname)} for f in FEEDS]
    response = {
        'did': config.SERVICE_DID,
        'feeds': feeds
    }
    return jsonify(response)


@app.get('/xrpc/app.bsky.feed.getFeedSkeleton')
def get_feed_skeleton():
    feed_uri = request.args.get('feed', default=None, type=str)
    if not feed_uri :
        return '', 404
    
    if config.OWNER_DID not in feed_uri :
        return '', 404
    
    feed = feed_uri.split('/')[-1]
    logger.info(f"Feed = {feed}")

    feed_data = find_feed(feed)
    if not feed_data:
        return 'unkown feed', 400

    try:
        cursor = request.args.get('cursor', default=None, type=str)
        limit = request.args.get('limit', default=20, type=int)
        body = compute_feed(feed_data, cursor, limit)
    except ValueError as e:
        return str(e), 400

    return jsonify(body)

if __name__ == '__main__' :
    options : Dict[str, Any] = {}

    if config.WAITRESS_PREFIX:
        options["url_prefix"] = config.WAITRESS_PREFIX

    listen = config.WAITRESS_LISTEN

    if listen:
        if listen.startswith("/"):
            options["unix_socket"] = listen
            options["unix_socket_perms"] = '660'
        else :
            options["listen"] = listen

    print(f"startup options = {options}")

    if os.getenv("FLASK_ENV") == "production":
        from waitress import serve
        serve(app, **options)
    else :
        app.run(debug=True)
