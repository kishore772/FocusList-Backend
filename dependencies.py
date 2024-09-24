# app/dependencies.py
from fastapi import Header, HTTPException, Security, status
from utils.auth_utils import verify_token

async def get_current_user(token: str = Security(...)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return verify_token(token, credentials_exception)
