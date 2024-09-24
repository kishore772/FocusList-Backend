from fastapi import APIRouter, Depends, HTTPException, status, Security
from sqlalchemy.ext.asyncio import AsyncSession
from configuration.database import get_db
from services.user_service import UserService
from schemas.user_schema import UserCreate, UserRead, UserLogin, UserUpdate
from utils.auth_utils import create_access_token
from datetime import timedelta
from configuration.database import ACCESS_TOKEN_EXPIRE_MINUTES
from utils.auth_utils import validate_token, access_validator

router = APIRouter()

async def get_authenticate(token: dict = Depends(validate_token)):
    return token


@router.post("/signup/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    
    # Check if the user already exists (by username or email)
    existing_user = await user_service.get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create the new user
    created_user = await user_service.create_user(user)
    
    return created_user

@router.post("/login/", response_model=dict)
async def login_for_access_token(form_data: UserLogin, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    user = await user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"user_id": user.id}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Example protected route with token validation
@router.get("/users", response_model=list[UserRead])
async def get_all_users(
    db: AsyncSession = Depends(get_db), 
    current_user: dict=Depends(get_authenticate)
):
    user_service = UserService(db)
    created_by = current_user["user_id"]
    users = await user_service.get_all_users()
    return users

# API to get a user by ID
@router.get("/users/{user_id}", response_model=UserRead)
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db), current_user: dict=Depends(get_authenticate)):
    user_service = UserService(db)
    created_by = current_user["user_id"]

    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# API to update a user by ID
@router.put("/users/{user_id}", response_model=UserRead)
async def update_user(user_id: int, user_data: UserUpdate, db: AsyncSession = Depends(get_db), current_user: dict=Depends(get_authenticate)):
    user_service = UserService(db)
    created_by = current_user["user_id"]

    updated_user = await user_service.update_user(user_id, user_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found or update failed")
    return updated_user

#can use for access validator authentication type
# Example protected route with token validation and access control
@router.get("/admin", dependencies=[Security(access_validator, scopes=["admin"])])
async def admin_panel(token: dict = Depends(validate_token)):
    return {"message": "Welcome to the admin panel"}
