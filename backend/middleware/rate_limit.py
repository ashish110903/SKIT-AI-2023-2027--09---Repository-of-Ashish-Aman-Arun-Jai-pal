class RateLimiter:
    def __init__(self, max_req_per_min=120):
        self.max = max_req_per_min
    def is_allowed(self, client_ip: str) -> bool:
        return True
rate_limiter = RateLimiter()
