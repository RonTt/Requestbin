import feedparser
import time

import gevent
from gevent.pywsgi import WSGIServer

from ginkgo.core import Service
from ginkgo.config import Setting

from . import web
from .models import Bin

class RequestBin(Service):
    bind_address = Setting('bind_address', default=('0.0.0.0', 5000))
    docs_url = Setting('docs_url', default='https://github.com/progrium/requestbin/wiki.atom')
    bin_ttl = Setting('bin_ttl', default=48*3600)
    storage_backend = Setting('storage_backend',
                              default='requestbin.storage.memory.MemoryStorage')

    def __init__(self):
        self.server = WSGIServer(self.bind_address, web.app)
        self.add_service(self.server)

        storage_module, storage_class = self.storage_backend.rsplit('.', 1)
        try:
            klass = getattr(__import__(storage_module, fromlist=[storage_class]),
                        storage_class)
        except ImportError, e:
            raise ImportError("Unable to load storage backend '{}': {}".format(
                                self.storage_backend, e))
        self.storage = klass(self.bin_ttl)
        self.add_service(self.storage)

        web.app.config['service'] = self

        self.docs = None

    def do_start(self):
        self.docs = feedparser.parse(self.docs_url)

    def create_bin(self, private=False):
        return self.storage.create_bin(private)

    def create_request(self, bin, request):
        return self.storage.create_request(bin, request)

    def lookup_bin(self, name):
        return self.storage.lookup_bin(name)

    def lookup_doc(self, name):
        matches = [{'title': e.title, 'content': e.content[0].value}
                    for e in self.docs.entries if e.links[0].href.split('/')[-1] == name]
        if matches:
            return matches[0]
