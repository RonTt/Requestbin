from __future__ import absolute_import

import time
import cPickle as pickle

import redis
from ginkgo import Service
from ginkgo import Setting

from ..models import Bin

class RedisStorage(Service):
    prefix = Setting('redis_prefix', default='requestbin')
    redis_init = Setting('redis_init', default={
                            'host': 'localhost', 'port': 6379, 'db': 0})

    def __init__(self, bin_ttl):
        self.bin_ttl = bin_ttl
        self.redis = redis.StrictRedis(**self.redis_init)

    def _key(self, name):
        return '{}_{}'.format(self.prefix, name)

    def _request_count_key(self):
        return '{}-requests'.format(self.prefix)

    def create_bin(self, private=False):
        bin = Bin(private)
        key = self._key(bin.name)
        self.redis.setex(key, self.bin_ttl, bin.dump())
        return bin

    def create_request(self, bin, request):
        bin.add(request)
        key = self._key(bin.name)
        self.redis.set(key, bin.dump())
        self.redis.setnx(self._request_count_key(), 0)
        self.redis.incr(self._request_count_key())

    def count_bins(self):
        keys = self.redis.keys("{}_*".format(self.prefix))
        return len(keys)

    def count_requests(self):
        return int(self.redis.get(self._request_count_key()) or 0)

    def lookup_bin(self, name):
        key = self._key(name)
        serialized_bin = self.redis.get(key)
        try:
            return Bin.load(serialized_bin)
        except TypeError:
            self.redis.delete(key) # clear bad data
            raise KeyError("Bin not found")
