from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from starlette.requests import Request
from secrets import token_hex

from app.kernel.domain.exceptions import AuthErrorException
from app.config.apiconfig import current_config

ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def gen_hashed_password(paswd: str):
    return pwd_context.hash(paswd)


def verify_password(paswd: str, hashed_paswd: str):
    return pwd_context.verify(paswd, hashed_paswd)


def create_access_token(
    data: dict, jwt_secret_key: str, expires_delta: timedelta | None = None
):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=60)

    to_encode = {"exp": expire, **data}
    encoded_jwt = jwt.encode(to_encode, jwt_secret_key, algorithm=ALGORITHM)
    return encoded_jwt


def decode_jwt(token: str | None, jwt_secret_key: str) -> str | None:
    if token is None:
        return None

    try:
        decode_jwt = jwt.decode(token, jwt_secret_key, algorithms=[ALGORITHM])

        return decode_jwt

    except JWTError:
        return None

def generate_code(nbytes: int = 16) -> bytes:
    code = token_hex(nbytes)
    return code.encode("utf-8")

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        credentials = await super().__call__(request)

        if credentials:
            if not credentials.scheme.lower() == "bearer":
                raise AuthErrorException("Invalid authentication scheme!")

            if not decode_jwt(credentials.credentials, current_config.jwt_secret_key):
                raise AuthErrorException("Invalid token!")

            return credentials.credentials

        else:
            raise AuthErrorException("Invalid authorization code!")
