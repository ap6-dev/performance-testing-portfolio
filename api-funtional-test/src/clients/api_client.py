import requests
import logging
import time

logger = logging.getLogger(__name__)

def measure_time(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        duration = end - start
        logging.info(f"[PERF] {func.__name__} took {duration*1000:.1f} ms\n")
        return result
    return wrapper

#--------------------------
# API Client
#--------------------------
class APIClient:
    
    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self.session = requests.Session() #Reuse TCP Connection for tests
        self.headers = headers or {}

    def _request(self, method, endpoint, **kwargs):
        full_url = self.base_url + endpoint
        headers = self.headers
        
        return self.session.request(method, full_url, **kwargs)
    
    @measure_time
    def get(self, endpoint, **kwargs):
        logger.info(f"GET {self.base_url + endpoint}")
        return self._request("GET", endpoint, **kwargs)
    
    @measure_time
    def post(self, endpoint, **kwargs):
        logger.info(f"POST {self.base_url + endpoint}")
        return self._request("POST", endpoint, **kwargs)

    @measure_time
    def put(self, endpoint, **kwargs):
        logger.info(f"PUT {self.base_url + endpoint}")
        return self._request("PUT", endpoint, **kwargs)

    @measure_time
    def delete(self, endpoint, **kwargs):
        logger.info(f"DELETE {self.base_url + endpoint}")
        return self._request("DELETE", endpoint, **kwargs)


