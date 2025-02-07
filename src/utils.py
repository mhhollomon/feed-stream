import src.config as config

def at_post_uri(acct_did : str, collection : str, key : str) -> str :
    return f"at://{acct_did}/{collection}/{key}"

def at_feed_uri(feedname : str) -> str :
    return f"at://{config.OWNER_DID}/app.bsky.feed.generator/{feedname}"
