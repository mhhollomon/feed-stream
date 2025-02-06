import datetime

import peewee

db = peewee.SqliteDatabase('feed_database.sqlite3')


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Post(BaseModel):
    uri = peewee.CharField(index=True)
    cid = peewee.CharField()
    author = peewee.CharField()
    feed = peewee.CharField(index=True)
    indexed_at = peewee.DateTimeField(default=lambda: datetime.datetime.now(datetime.timezone.utc))


class SubscriptionState(BaseModel):
    service = peewee.CharField(unique=True)
    cursor = peewee.BigIntegerField()


if db.is_closed():
    db.connect()
    db.create_tables([Post, SubscriptionState])