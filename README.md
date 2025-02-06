# feed-stream
atproto feed generator based on jetstream

Multiple feeds will be supported.

# Reader (working)

Opens a websocket on the Jetstream. Only subscribes to posts (not likes, follows, etc)

For each messages see if it is wanted and writes a row to the `post` table if so.

# Server (not started)

Responds to queries for the list of posts in the feed.

## technologies
- [BlueSky Jetstream](https://github.com/bluesky-social/jetstream)
- [peewee](https://docs.peewee-orm.com/en/latest/) on top of sqlite
- [sqlite](https://sqlite.org/)