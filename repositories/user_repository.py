# app/repositories/user_repository.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user_model import User
from datetime import datetime
from sqlalchemy.orm import Session

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, username: str, email: str, hashed_password: str):
        new_user = User(username=username, email=email, hashed_password=hashed_password)
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user

    async def get_user_by_username(self, username: str):
        result = await self.db.execute(select(User).filter(User.username == username))
        return result.scalar_one_or_none()

    async def get_all_users(self):
        result = await self.db.execute(select(User))
        return result.scalars().all()

    async def get_user_by_id(self, user_id: int):
        result = await self.db.execute(select(User).filter(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str):
        result = await self.db.execute(select(User).filter(User.email == email))
        return result.scalar_one_or_none()

    async def update_user(self, user_id: int, user_data):
        user = await self.get_user_by_id(user_id)
        if user:
            if user_data.username:
                user.username = user_data.username
            if user_data.email:
                user.email = user_data.email
            if user_data.password:
                user.hashed_password = user_data.password  # Remember to hash passwords!
            await self.db.commit()
            await self.db.refresh(user)
        return user

    async def delete_user(self, user_id: int):
        user = await self.get_user_by_id(user_id)
        if user:
            await self.db.delete(user)
            await self.db.commit()
