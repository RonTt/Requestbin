import copy
import json
import time
import datetime
import os

import msgpack

from ginkgo import Setting

from .util import random_color
from .util import tinyid
from .util import solid16x16gif_datauri

class Bin(object):
    max_requests = Setting('max_requests', default=20)

    def __init__(self, private=False):
        self.created = time.time()
        self.private = private
        self.color = random_color()
        self.name = tinyid(8)
        self.favicon_uri = solid16x16gif_datauri(*self.color)
        self.requests = []
        self.secret_key = os.urandom(24) if self.private else None

    def json(self):
        return json.dumps(dict(
            private=self.private, 
            color=self.color, 
            name=self.name,
            request_count=len(self.requests)))
#            requests=self.requests,

    def dump(self):
        o = copy.copy(self.__dict__)
        o['requests'] = [r.dump() for r in self.requests]
        return msgpack.dumps(o)

    @staticmethod
    def load(data):
        o = msgpack.loads(data)
        o['requests'] = [Request.load(r) for r in o['requests']]
        b = Bin()
        b.__dict__ = o
        b.request_count = len(b.requests);
        return b


    def add(self, request):
        self.requests.insert(0, Request(request))
        if len(self.requests) > self.max_requests:
            for _ in xrange(self.max_requests, len(self.requests)):
                self.requests.pop(self.max_requests)

class Request(object):
    ignore_headers = Setting('ignore_headers', default=[])

    def __init__(self, input=None):
        if input:
            self.id = tinyid(6)
            self.time = time.time()
            self.remote_addr = input.headers.get('X-Forwarded-For',
                    input.remote_addr)
            self.method = input.method
            self.headers = dict(input.headers)
            for header in self.ignore_headers:
                self.headers.pop(header, None)
            self.query_string = input.query_string
            self.form_data = []
            for k in input.values:
                self.form_data.append([k, input.values[k]])
            self.body = input.data
            self.path = input.path
            self.content_length = input.content_length
            self.content_type = input.content_type

    @property
    def created(self):
        return datetime.datetime.fromtimestamp(self.time)

    def dump(self):
        return msgpack.dumps(self.__dict__)

    @staticmethod
    def load(data):
        r = Request()
        r.__dict__ = msgpack.loads(data)
        return r

    def __iter__(self):
        out = []
        if self.form_data:
            if hasattr(self.form_data, 'items'):
                items = self.form_data.items()
            else:
                items = self.form_data
            for k,v in items:
                try:
                    outval = json.dumps(json.loads(v), sort_keys=True, indent=2)
                except (ValueError, TypeError):
                    outval = v
                out.append((k, outval))
        else:
            try:
                out = (('body', json.dumps(json.loads(self.body), sort_keys=True, indent=2)),)
            except (ValueError, TypeError):
                out = (('body', self.body),)

        # Sort by field/file then by field name
        files = list()
        fields = list()
        for (k,v) in out:
            if type(v) is dict:
                files.append((k,v))
            else:
                fields.append((k,v))
        return iter(sorted(fields) + sorted(files))

