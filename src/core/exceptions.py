from .http_responses import error_responses

class BadRequestException(Exception):
    def __init__(self, text: str = error_responses[400]['description']):
        self.text = text
        
class UnauthorizedException(Exception):
    def __init__(self, text: str = error_responses[401]['description']):
        self.text = text
        
class NotFoundException(Exception):
    def __init__(self, text: str = error_responses[404]['description']):
        self.text = text