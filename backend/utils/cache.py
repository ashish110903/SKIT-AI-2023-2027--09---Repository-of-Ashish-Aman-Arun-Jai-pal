import time

class SimpleCache:
    def __init__(self, ttl=5):
        self.ttl = ttl
        self.store = {}
    def get(self, k):
        item = self.store.get(k)
        if item and time.time() - item['ts'] < self.ttl: return item['v']
        return None
    def set(self, k, v):
        self.store[k] = {'v': v, 'ts': time.time()}
