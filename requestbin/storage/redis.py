import time

import redis
import gevent
from gservice.core import Service
from gservice.config import Setting

from ..models import Bin

class RedisStorage(Service):
    redis_init = Setting('redis_init', default={
                            'host': 'localhost', 'port': 6379, 'db': 0})

    def __init__(self, bin_ttl):
        self.bin_ttl = bin_ttl
        self.redis = redis.StrictRedis(**self.redis_init)
