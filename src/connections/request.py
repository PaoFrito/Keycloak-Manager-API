import requests

def request(method: str, url: str, headers = None, data = None):
        
        if method == 'get':
            return requests.get(url, headers=headers, data=data)
        if method == 'post':
            return requests.post(url, headers=headers, data=data)
        if method == 'delete':
            return requests.delete(url, headers=headers, data=data)
        
        raise Exception("Method not allowed")