import requests
import json

class APIClient:
    
    def __init__(self, base_url, headers=None):
        self.base_url = base_url
        self.headers = headers or {}

    def _request(self, method, endpoint, **kwargs):
        full_url = self.base_url + endpoint
        headers = self.headers
        
        return requests.request(method, full_url, **kwargs)
    
    def get(self, endpoint, **kwargs):
        return self._request("GET", endpoint, **kwargs)