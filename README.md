# feed-stream
atproto feed generator based on jetstream

Multiple feeds are supported.

However, only posts (not likes and follows) are currently consumed.

## Reader (working)

Opens a websocket on the Jetstream. Only subscribes to posts (not likes, follows, etc)

For each message, sees if it is wanted and writes a row to the `post` table if so.

## Server (working)

Responds to queries for the list of posts in the feed.

## technologies
- [BlueSky Jetstream](https://github.com/bluesky-social/jetstream)
- [peewee](https://docs.peewee-orm.com/en/latest/) on top of sqlite
- [sqlite](https://sqlite.org/)

## LICENSE

This code is licensed un the MIT license see [LICENSE](LICENSE) for details.

Some portions of the source are adapted from [MarshalX's BlueSkyGenerator](https://github.com/MarshalX/bluesky-feed-generator) and is used by permission under the MIT license. See the [repository's LICENSE] (https://github.com/MarshalX/bluesky-feed-generator/LICENSE) file for details.