# app/utils/auth_utils.py
from datetime import datetime, timedelta
import os
from fastapi import Request, HTTPException, Depends
from jose import jwt, JWTError
from configuration.database import SECRET_KEY, ALGORITHM
from utils.error_response import ErrorResponse
from common.logging import logger
from fastapi.security import SecurityScopes, HTTPBearer, HTTPAuthorizationCredentials

# OAuth2 scheme to extract the token from the Authorization header
bearer_scheme = HTTPBearer()

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=2)  # Default to 15 minutes if no expiry is provided
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        return user_id
    except jwt.PyJWTError:
        raise credentials_exception
    
# Token validation function to decode and validate the JWT
async def validate_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials  # Extract the token from the Bearer scheme
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decode the JWT token using the secret key and algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)  # Add a debug print to check the token payload content
    
        user_id: str = payload.get("user_id")
        if user_id is None:
            logger.error("Invalid token: user_id is missing.")
            raise credentials_exception
        
        # Return the payload (e.g., user_id)
        return payload
    except JWTError as e:
        logger.error(f"Token validation failed: {str(e)}")
        raise credentials_exception
        
async def access_validator(security_scopes: SecurityScopes, payload: dict = Depends(validate_token)):
    # Example: Check if the payload contains the necessary scopes/roles
    if "scopes" not in payload:
        raise HTTPException(detail="No scopes provided in token.", status_code=403)

    user_scopes = payload["scopes"]
    
    # Check if the user has any of the required scopes
    access = list(set(user_scopes) & set(security_scopes.scopes))
    
    if not access:
        raise HTTPException(detail="Access denied. Insufficient privileges.", status_code=403)
