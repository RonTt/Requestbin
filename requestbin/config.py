import os, urlparse
DEBUG = True
REALM = os.environ.get('REALM', 'local')

ROOT_URL = "http://localhost:3000"

PORT_NUMBER = 4000

FLASK_SESSION_SECRET_KEY = "N1BKhJLnBqLpexOZdklsfDKFJDKFadsfs9a3r324YB7B73AglRmrHMDQ9RhXz35"

REDIS_URL = ""
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_DB = 2

if REALM == 'prod':
    DEBUG = True
    ROOT_URL = "http://requestb.in"

    REDIS_URL = os.environ.get("REDISCLOUD_URL")
    redis_url = urlparse.urlparse(REDIS_URL)
    REDIS_HOST = redis_url.hostname
    REDIS_PORT = redis_url.port
    REDIS_PASSWORD = redis_url.password
    REDIS_DB = 0