# app/routers/task_router.py
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from configuration.database import get_db
from services.task_service import TaskService
from schemas.task_schema import TaskCreate, TaskRead, TaskUpdate
from utils.auth_utils import validate_token
from typing import List

router = APIRouter()

# Mock function to get current authenticated user
# This should be replaced by your actual authentication logic
async def get_current_user(token: dict = Depends(validate_token)):
    return token

#Create Task
@router.post("/tasks/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    task_service = TaskService(db)
    
    # Extract the user_id from the token
    created_by = current_user["user_id"]
    
    # Ensure the user_id is present and valid
    if created_by is None:
        raise HTTPException(status_code=400, detail="User ID is missing from token")
    
    # Create the task and return with the user's email in 'creator'
    return await task_service.create_task(task, created_by)



# Get All Tasks
@router.get("/tasks/", response_model=List[TaskRead], status_code=status.HTTP_200_OK)
async def get_tasks(db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    task_service = TaskService(db)
    
    created_by = current_user["user_id"]
    
    if created_by is None:
        raise HTTPException(status_code=400, detail="User ID is missing from token")
    
    return await task_service.get_tasks(created_by)

@router.get("/tasks/all", response_model=List[TaskRead], status_code=status.HTTP_200_OK)
async def get_tasks_by_category(status: str = None, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    task_service = TaskService(db)
    
    created_by = current_user["user_id"]
    
    if created_by is None:
        raise HTTPException(status_code=400, detail="User ID is missing from token")
    
    if status:
        # Fetch tasks filtered by status/category
        return await task_service.get_tasks_status(created_by, status)
    else:
        # Fetch all tasks
        return await task_service.get_tasks(created_by)


# Get Task by ID
@router.get("/tasks/{task_id}", response_model=TaskRead, status_code=status.HTTP_200_OK)
async def get_task_by_id(task_id: int, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    task_service = TaskService(db)
    
    # Extract the user_id (created_by) from the current user
    created_by = current_user.get("user_id")
    
    # Ensure the user_id is present and valid
    if created_by is None:
        raise HTTPException(status_code=400, detail="User ID is missing from token")
    
    # Fetch the task by id and created_by (user_id)
    return await task_service.get_task_by_id(task_id, created_by)

# Update Task
@router.put("/tasks/{task_id}", response_model=TaskRead, status_code=status.HTTP_200_OK)
async def update_task(task_id: int, task_data: TaskUpdate, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    task_service = TaskService(db)
    
    # Extract user_id (created_by) from the current user
    created_by = current_user.get("user_id")
    
    if created_by is None:
        raise HTTPException(status_code=400, detail="User ID is missing from token")
    
    # Pass the user_id (created_by) along with task data and task_id to the service
    return await task_service.update_task(task_data, task_id, created_by)


# Delete Task
@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db), current_user: dict = Depends(get_current_user)):
    task_service = TaskService(db)
    
    created_by = current_user.get("user_id")
    
    if created_by is None:
        raise HTTPException(status_code=400, detail="User ID is missing from token")
    
    return await task_service.delete_task(task_id, created_by)
