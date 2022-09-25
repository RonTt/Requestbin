from interactions.request import RequestClient

class WebhookFacts(object):
    _request = RequestClient()
    _resource = "bins"
    
    @classmethod
    def create_bin(cls, key):
        data = {'key': f'{key}'}
        status, header, body = cls._request.post(cls._resource, data)
        
        return status, header, body

        
        
        
        
        