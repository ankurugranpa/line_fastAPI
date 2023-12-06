from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship

from api.db import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    text_message = Column(String(1024))

    done = relationship("Done", back_populates="task", cascade="delete")


class Done(Base):
    __tablename__ = "dones"

    id = Column(Integer, ForeignKey("tasks.id"), primary_key=True)

    task = relationship("Task", back_populates="done")


class Message(Base):
    __tablename__ = "message"
    id =  Column(Integer, primary_key=True)
    user_id = Column(String(17), nullable=False)
    message = Column(Text(10000))

