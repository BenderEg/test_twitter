# redis connection data
REDIS__HOST=twitter-red
REDIS__PORT=6379
REDIS__DB=0

# postgres connection data localhost

POSTGRES__SCHEMA=content
POSTGRES__PASSWORD=password
POSTGRES__USER=admin
POSTGRES__DB=twitter
POSTGRES__HOST=twitter-db
POSTGRES__PORT=5432

# sqlalchemy mode

ECHO=False

# logging

LOG_LEVEL=WARNING

# App

FEED_PARTITIONS=10
TWIT_NUMBERS=5
MAX_TWITS=500
BASE_URL=http://twitter-app:8000