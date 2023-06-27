from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from jose.jwt import decode as jwt_decode
from jose.jwt import encode as jwt_encode
from sqlalchemy.orm import Session

from app.crud.user_crud import select_user_by_username_db
from app.models import User
from app.session import get_db
from app.setting import ACCESS_TOKEN_EXPIRE_HOURS, ALGORITHM, SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/v1/auth/token')


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt_encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt, expire


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt_decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_exp: int = payload.get("exp")
        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid authentication token1")
        user = select_user_by_username_db(db, username)

        if user is None:
            raise HTTPException(status_code=401, detail="Invalid username")

        if check_expire_token(user, token_exp):
            return user
        else:
            delete_token_user(db=db, user=user)
            raise HTTPException(status_code=401, detail="Token expired")

    except JWTError:
        user = db.query(User).filter(User.token == token).first()
        delete_token_user(db=db, user=user)
        raise HTTPException(status_code=401, detail="Token expired")


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
