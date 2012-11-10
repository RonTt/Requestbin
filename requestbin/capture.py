import sys

import teena
import gevent.pywsgi

from StringIO import StringIO
from peak.util.proxies import ObjectWrapper

class ReadCaptureWrapper(ObjectWrapper):
    capture = None

    def __init__(self, rfile):
        ObjectWrapper.__init__(self, rfile)
        self.capture = StringIO()

    def read(self, size=-1):
        subject = object.__getattribute__(self, '__subject__')
        data = subject.read(size)
        self.capture.write(data)
        return data

    def readline(self, size=-1):
        subject = object.__getattribute__(self, '__subject__')
        data = subject.readline(size)
        self.capture.write(data)
        return data

class RawCaptureWSGIHandler(gevent.pywsgi.WSGIHandler):
    def handle_one_request(self):
        self.rfile = ReadCaptureWrapper(self.rfile)
        return super(self.__class__, self).handle_one_request()

    def get_environ(self):
        environ = super(self.__class__, self).get_environ()
        environ['raw'] = self.rfile.capture
        return environ
