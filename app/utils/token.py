from jose import JWTError
from jose.jwt import decode as jwt_decode, encode as jwt_encode
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.crud.user_crud import select_user_by_username_db
from app.session import get_db
from app.models import User


SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/v1/auth/token')


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt_encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt, expire


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt_decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_exp: int = payload.get("exp")
        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication token")
        user = select_user_by_username_db(db, username)

        if user is None:
            raise HTTPException(status_code=401, detail="Invalid username")

        if check_expire_token(user, token_exp):
            return user
        else:
            delete_token_user(db=db, user=user)
            raise HTTPException(status_code=401, detail="Token expired")

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid authentication token")


def delete_token_user(db: Session, user: User):
    user.is_active = False
    user.exp_token = None
    user.token = None
    db.commit()
    db.refresh(user)


def check_expire_token(user: User, exp_token: int):
    expire_token = datetime.utcfromtimestamp(exp_token)
    expire_token_str = expire_token.strftime("%Y-%m-%d %H:%M:%S")
    user_expire_token_str = user.exp_token.strftime("%Y-%m-%d %H:%M:%S")
    if expire_token_str == user_expire_token_str:
        return True
    return False
