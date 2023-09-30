from typing import Any, Dict, Optional
from fastapi import HTTPException, status

class AuthErrorException(HTTPException):
    def __init__(self, detail: Any = None, headers: Optional[Dict[str, str]] | None = None) -> None:
        super().__init__(status.HTTP_403_FORBIDDEN, detail, headers)
        
class EntityNotFoundException(HTTPException):
    def __init__(self, headers: Optional[Dict[str, str]] | None = None) -> None:
        super().__init__(status.HTTP_404_NOT_FOUND, 'Entity not found!', headers)
        
    
class EntityExists(HTTPException):
    def __init__(self, headers: Optional[Dict[str, str]] | None = None) -> None:
        super().__init__(status.HTTP_400_BAD_REQUEST, 'Entity already exists!', headers)
        