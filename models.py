import os
import datetime

from peewee import *

if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
    # These environment variables are configured in app.yaml.
    CLOUDSQL_CONNECTION_NAME = os.environ.get('CLOUDSQL_CONNECTION_NAME')
    CLOUDSQL_USER = os.environ.get('CLOUDSQL_USER')
    CLOUDSQL_PASSWORD = os.environ.get('CLOUDSQL_PASSWORD')

    # Connect using the unix socket located at
    # /cloudsql/cloudsql-connection-name.
    cloudsql_unix_socket = os.path.join(
        '/cloudsql', CLOUDSQL_CONNECTION_NAME)
    print 'here'

    database = MySQLDatabase(
        'nlp',
        unix_socket=cloudsql_unix_socket,
        user=CLOUDSQL_USER,
        password=CLOUDSQL_PASSWORD)
else:
    database = MySQLDatabase(
        'nlp',
        user='root',
        password='root',
        host='localhost',
        thread_safe=True
    )


class BaseModel(Model):
    created_on = DateTimeField(default=datetime.datetime.now)
    updated_on = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = database


class Article(BaseModel):
    headline = CharField()
    url = CharField()
    sentiment_score = CharField(default="")
    sentiment_polarity = CharField(default="")
    sentiment_magnitude = CharField(default="")


class Sentence(BaseModel):
    text = TextField()
    begin_offset = CharField()
    sentiment_score = CharField()
    sentiment_polarity = CharField()
    sentiment_magnitude = CharField()
    article = ForeignKeyField(Article, backref='sentences')


database.connect()
database.create_tables([Article, Sentence], safe=True)
database.close()
