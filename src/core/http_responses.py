from fastapi import status
from typing import Any, Dict
from dataclasses import dataclass

@dataclass
class Response():
    code: int
    description: str
   
success_responses: Dict = {
    200: Response(code=status.HTTP_200_OK, description="OK").__dict__,
    201: Response(code=status.HTTP_201_CREATED, description="Created").__dict__,
    204: Response(code=status.HTTP_204_NO_CONTENT, description="No content").__dict__,
}

error_responses: Dict = {
    400: Response(code=status.HTTP_400_BAD_REQUEST, description="Bad Request").__dict__,
    401: Response(code=status.HTTP_401_UNAUTHORIZED, description="Unauthorized").__dict__,
    404: Response(code=status.HTTP_404_NOT_FOUND, description="Not Found").__dict__,
    500: Response(code=status.HTTP_500_INTERNAL_SERVER_ERROR, description="Internal Server Error").__dict__
}