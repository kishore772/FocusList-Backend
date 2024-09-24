from repositories.user_repository import UserRepository
from passlib.context import CryptContext
from schemas.task_schema import TaskCreate
from schemas.user_schema import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, db):
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
            "creator": creator_email  # Return the user's email as creator
        }
    async def get_user_by_email(self, email: str):
        # Fetch a user by email to ensure it doesn't already exist
        return await self.user_repository.get_user_by_email(email)

    async def authenticate_user(self, username: str, password: str):
        # Fetch the user from the database by username
        user = await self.user_repository.get_user_by_username(username)
        if not user:
            return None
        # Verify if the password matches the hashed password stored in the database
        if not self.verify_password(password, user.hashed_password):
            return None
        return user

    async def create_user(self, user_data: UserCreate):
        hashed_password = self.hash_password(user_data.password)  # Hash the password before saving
        return await self.user_repository.create_user(user_data.username, user_data.email, hashed_password)

    async def get_all_users(self):
        return await self.user_repository.get_all_users()

    async def get_user_by_id(self, user_id: int):
        return await self.user_repository.get_user_by_id(user_id)

    async def update_user(self, user_id: int, user_data):
        if user_data.password:
            user_data.password = self.hash_password(user_data.password)
        return await self.user_repository.update_user(user_id, user_data)

    async def delete_user(self, user_id: int):
        return await self.user_repository.delete_user(user_id)

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
