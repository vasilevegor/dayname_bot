from datetime import datetime, date
import datetime

from sqlalchemy import Column, ForeignKey, Integer, VARCHAR, DATE, String, BigInteger, select
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker

from .base import BaseModel

default_foreword = "Погоняло дня"

class Chat(BaseModel):
    __tablename__ = 'chats'
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True, nullable=False)
    
    chat_id: Mapped[int] = mapped_column(BigInteger, unique=False, nullable=False)

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id"), unique=False, nullable=False)
    
    role: Mapped[int] = mapped_column(Integer, default=0, unique=False, nullable=False)

    nickname: Mapped[str] = mapped_column(String(32), unique=False)
    
    foreword: Mapped[str] = mapped_column(String(32), default=default_foreword, unique=False)

    def __str__(self):
        return f"<User:{self.user_id}>"

    def __repr__(self):
        return self.__str__()


async def get_chat(chat_id: int, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(select(Chat)
                                           .where(Chat.chat_id == chat_id)
                                           .order_by(Chat.id.desc()))
            return result
        
        
async def set_chat(chat_id: int, user_id: int, role: int = 0, nickname: str, foreword: str = default_foreword, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            chat = Chat(chat_id=chat_id,
                        user_id=user_id,
                        role=role,
                        nickname=nickname,
                        foreword=foreword
                        )
            session.add(chat)