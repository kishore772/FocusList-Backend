# app/models/task_model.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from configuration.database import Base
from datetime import datetime, timezone
from models.user_model import User

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False)  # 'TODO', 'InProgress', 'Completed'
    date_time = Column(DateTime(timezone=True), default=datetime.now(timezone.utc))
    created_by = Column(Integer, ForeignKey(User.id))
