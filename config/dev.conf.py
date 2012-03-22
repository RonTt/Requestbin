bind_address = ('0.0.0.0', 5000)
#storage_backend = 'requestbin.storage.redis.RedisStorage'

def service():
    from requestbin.service import RequestBin
    return RequestBin()
