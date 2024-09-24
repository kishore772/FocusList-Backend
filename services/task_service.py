from repositories.task_repository import TaskRepository
from repositories.user_repository import UserRepository
from schemas.task_schema import TaskCreate
from datetime import datetime
from fastapi import HTTPException
from schemas.task_schema import TaskUpdate

class TaskService:
    def __init__(self, db):
        self.db = db

        self.task_repository = TaskRepository(db)
        self.user_repository = UserRepository(db)

    async def create_task(self, task_data: TaskCreate, created_by: int):
        # Create the task via the repository
        new_task = await self.task_repository.create_task(task_data, created_by)
        
        # Fetch the user email from the repository
        creator_email = await self.task_repository.get_user_email(created_by)
        
        # Return the task details along with the creator's email
        return {
            "id": new_task.id,
            "name": new_task.name,
            "status": new_task.status,
            "date_time": new_task.date_time,
            "created_by": new_task.created_by,  # Return the user_id in created_by
            "creator": creator_email  # Return the user's email as creator
        }

    async def get_tasks(self, user_id: int):
        
        tasks = await self.task_repository.get_tasks_by_user(user_id)
        
        if not tasks:
            return []
        
        if not tasks:
            raise HTTPException(status_code=404, detail="Task not found")
        
        creator_email = await self.task_repository.get_user_email(user_id)
                
        task_list = []
        for t in tasks:
            task_list.append({
                "id": t.id,
                "name": t.name,
                "status": t.status,
                "date_time": t.date_time,
                "created_by": t.created_by,  # user_id
                "creator": creator_email  # user email
            })
            
        return task_list
    
    async def get_tasks_status(self, created_by: int, status: str = None):
        # Fetch tasks filtered by status if status is provided, otherwise fetch all tasks
        if status:
            tasks = await self.task_repository.get_tasks_by_status(created_by, status)
        else:
            tasks = await self.task_repository.get_all_tasks(created_by)
        
        # If no tasks are found, return an empty list
        if not tasks:
            return []
        
        # Fetch the creator's email (assuming it's the same for all tasks of the user)
        creator_email = await self.task_repository.get_user_email(created_by)
        
        # Build the list of tasks with the desired format
        task_list = []
        for task in tasks:
            task_list.append({
                "id": task.id,
                "name": task.name,
                "status": self.get_task_status_label(task.status),  # Convert status to a readable format
                "date_time": task.date_time,
                "created_by": task.created_by,  # user_id
                "creator": creator_email  # user email
            })
        
        return task_list

    # Helper method to format the task status
    def get_task_status_label(self, status_code):
        status_labels = {
            'completed': 'Completed',
            'flagged': 'Flagged',
            'scheduled': 'Scheduled',
            'today': 'Today'
        }
        return status_labels.get(status_code, 'Unknown')

    async def get_task_by_id(self, task_id: int, user_id: int):
        # Fetch the task by task_id and check if it belongs to the user (user_id)
        task = await self.task_repository.get_task_by_id(task_id, user_id)

        
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        # Fetch the creator's email (from the user_id)
        creator_email = await self.task_repository.get_user_email(user_id)
        
        # Return task details with the creator's email
        return {
            "id": task.id,
            "name": task.name,
            "status": task.status,
            "date_time": task.date_time,
            "created_by": task.created_by,  # user_id
            "creator": creator_email  # user email
        }

    async def update_task(self, task_data: TaskUpdate, task_id: int, user_id: int):
        # Check if the task exists and is created by the current user (user_id)
        task = await self.task_repository.get_task_by_id(task_id)
        
        # Ensure that the task was created by the current user
        
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        # Update the task via the repository
        updated_task = await self.task_repository.update_task(task_data, task_id)
        
        # Fetch the user email from the repository
        creator_email = await self.task_repository.get_user_email(user_id)
        
        # Return the updated task along with the creator's email
        return {
            "id": updated_task.id,
            "name": updated_task.name,
            "status": updated_task.status,
            "date_time": updated_task.date_time,
            "created_by": updated_task.created_by,  # Return the user_id in created_by
            "creator": creator_email  # Return the user's email as creator
        }

    async def delete_task(self, task_id: int, user_id: int):
        task =  await self.task_repository.delete_task(task_id, user_id)
        
        # Ensure that the task was created by the current user
        
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
