from typing import Any, Dict, Optional
from fastapi import HTTPException, status


class CodeActivationExists(HTTPException):
    def __init__(self, headers: Optional[Dict[str, str]] | None = None) -> None:
        super().__init__(
            status.HTTP_403_FORBIDDEN, "An code activation exists!", headers
        )
