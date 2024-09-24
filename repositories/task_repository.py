from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from models.task_model import Task
from datetime import datetime
from fastapi import HTTPException
from schemas.task_schema import TaskCreate, TaskUpdate
from models.user_model import User


class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_task(self, task_data: TaskCreate, created_by: int):
                # Create the task
        new_task = Task(
            name=task_data.name,
            status=task_data.status,
            date_time=datetime.utcnow(),
            created_by=created_by
        )
        self.db.add(new_task)
        await self.db.commit()
        await self.db.refresh(new_task)
        return new_task

    async def get_user_email(self, user_id: int):
        # Fetch the user email by the user_id
        user = await self.db.get(User, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user.email


    async def get_tasks_by_user(self, user_id: int):
        result = await self.db.execute(select(Task).where(Task.created_by == user_id))
        return result.scalars().all()

    async def get_task_by_id(self, task_id: int, user_id: int):
        # Fetch the task by task_id and ensure it's owned by the given user_id
        query = await self.db.execute(
            select(Task).where(Task.id == task_id, Task.created_by == user_id)
        )
        return query.scalar_one_or_none()
    
    async def get_tasks_by_status(self, created_by: int, status: str):
        query = select(Task).where(Task.created_by == created_by, Task.status == status)
        result = await self.db.execute(query)
        return result.scalars().all()


    async def update_task(self, task_data: TaskUpdate, task_id: int):
        # Fetch the task to be updated
        task = await self.get_task_by_id(task_id)
        
        # Update task fields with the new data
        task.name = task_data.name
        task.status = task_data.status
        task.date_time = task_data.date_time
        
        # Save changes
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task
    
    async def delete_task(self, task_id: int, user_id: int):
        task = await self.get_task_by_id(task_id, user_id)
        if not task:
            return None

        await self.db.delete(task)
        await self.db.commit()
        return task
