
from . import feeddata, music
FEEDS = [
    music.feed
]

def find_feed(shortname : str | None) -> feeddata.FeedData | None :
    if shortname  :
        for f in FEEDS :
            if f.shortname  == shortname :
                return f
    
    return None