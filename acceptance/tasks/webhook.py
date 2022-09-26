from interactions.request import RequestClient 


class WebhookTask(object):
    _request = RequestClient()
    _resource = "bins"
    
    @classmethod
    def get_bin(cls, key):
        status, header, body = cls._request.get(cls._resource, key)
        return status, header, body
