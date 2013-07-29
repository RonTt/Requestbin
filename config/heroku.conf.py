import os
import urlparse

bind_address = ('0.0.0.0', int(os.environ.get("PORT", 4000)))
ignore_headers = """
X-Varnish
X-Forwarded-For
X-Heroku-Dynos-In-Use
X-Request-Start
X-Heroku-Queue-Wait-Time
X-Heroku-Queue-Depth
X-Real-Ip
X-Forwarded-Proto
X-Via
X-Forwarded-Port
""".split("\n")[1:-1]
storage_backend = 'requestbin.storage.redis.RedisStorage'

redis_url = urlparse.urlparse(os.environ.get("REDIS_URL", "redis://50.19.218.147:10043/0"))
redis_init = {
    'host': redis_url.hostname, 'port': redis_url.port, 'db': redis_url.fragment,
    'password': redis_url.password}

async = 'ginkgo.async.gevent'
service = "requestbin.service.RequestBin"
