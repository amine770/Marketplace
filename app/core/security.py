#-password hashing, verify password
#-create token and validation
from jose import JWTError, jwt
from pwdlib import PasswordHash
from typing import Dict, Any, Optional
from datetime import timedelta, datetime

from app.core.config import settings

pwd_context = PasswordHash.recommended()

def hash_password(plain_password: str) -> str:
    return pwd_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: Dict[str, Any], expiration_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expiration_delta:
        expire = datetime.utcnow() + expiration_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp":expire})
    encoded_token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_token

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
