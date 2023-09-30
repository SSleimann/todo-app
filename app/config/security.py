from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext


ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def gen_hashed_password(paswd: str):
    return pwd_context.hash(paswd)
    
def verify_password(paswd: str, hashed_paswd: str):
    return pwd_context.verify(paswd, hashed_paswd)

def create_access_token(data: dict, jwt_secret_key: str, expires_delta: timedelta | None = None):
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