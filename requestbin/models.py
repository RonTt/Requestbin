import collections
import json
import time
import datetime
import os

from ginkgo.config import Setting

from .util import random_color
from .util import tinyid
from .util import solid16x16gif_datauri

_bin_properties = """
created
private
color
name
favicon_uri
requests
secret_key
""".split("\n")[1:-1]

_request_properties = """
bin
id
headers
created
remote_addr
method
query_string
form_data
body
path
content_type
content_length
""".split("\n")[1:-1]

class Bin(collections.namedtuple("Bin", _bin_properties)):
    max_requests = Setting('max_requests', default=50)

    def __new__(cls, private=False):
        color = random_color()
        bin = super(Bin, cls).__new__(cls, **dict(
            created = time.time(),
            private = private,
            color = color,
            name = tinyid(8),
            favicon_uri = solid16x16gif_datauri(*color),
            requests = [],
            secret_key = os.urandom(24) if private else None,))
        return bin

    def json(self):
        return json.dumps(dict(
            private=self.private,
            color=self.color,
            name=self.name,
            requests=self.requests))

    def add(self, request):
        self.requests.insert(0, Request(self, request))
        if len(self.requests) > self.max_requests:
            for _ in xrange(self.max_requests, len(self.requests)):
                self.requests.pop(self.max_requests)

class Request(collections.namedtuple("Request", _request_properties)):
    ignore_headers = Setting('ignore_headers', default=[])

    def __new__(cls, bin, input):
        headers = dict(input.headers)
        for header in cls.ignore_headers:
            headers.pop(header, None)
        form_data = []
        for k in input.values:
            form_data.append([k, input.values[k]])
        request = super(Request, cls).__new__(cls, **dict(
            bin = bin,
            id = tinyid(6),
            created = datetime.datetime.now(),
            remote_addr = input.headers.get('X-Forwarded-For',
                input.remote_addr),
            method = input.method,
            headers = headers,
            query_string = input.query_string,
            form_data = form_data,
            body = input.data,
            path = input.path,
            content_length = input.content_length,
            content_type = input.content_type,))
        return request

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

