import requests
import logging

logger = logging.getLogger(__name__)

#--------------------------
# API Client
#--------------------------
class APIClient:
    
    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self.headers = headers or {}

    def _request(self, method, endpoint, **kwargs):
        full_url = self.base_url + endpoint
        headers = self.headers
        
        return requests.request(method, full_url, **kwargs)
    
    def get(self, endpoint, **kwargs):
        logger.info(f"GET {self.base_url + endpoint}")
        return self._request("GET", endpoint, **kwargs)
    
    def post(self, endpoint, **kwargs):
        logger.info(f"POST {self.base_url + endpoint}")
        return self._request("POST", endpoint, **kwargs)