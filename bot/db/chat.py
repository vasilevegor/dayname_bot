from datetime import datetime, date
import datetime

from sqlalchemy import (Column, ForeignKey, Integer, VARCHAR, 
                        DATE, String, BigInteger, select, delete)

from sqlalchemy.orm import Mapped, mapped_column, sessionmaker

from .base import BaseModel

default_foreword = "Погоняло дня"

class Chat(BaseModel):
    __tablename__ = 'chats'
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, unique=True, nullable=False)
    
    chat_id: Mapped[int] = mapped_column(BigInteger, unique=False, nullable=False)

    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.user_id"), unique=False, nullable=False)
    
    role: Mapped[int] = mapped_column(Integer, default=0, unique=False, nullable=False)

    nickname: Mapped[str] = mapped_column(String(32), unique=False, nullable=True)
    
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
            nickname_list = []
            foreword_list = []
            for nickname in result.scalars():
                if (nickname.nickname is None) or (nickname.foreword is None):
                    pass
                else:
                    nickname_list.append(nickname.nickname)
                
                foreword_list.append(nickname.foreword)
            return nickname_list, foreword_list
        
        
async def set_chat(chat_id: int, user_id: int, session_maker: sessionmaker, nickname: str = None, role: int = 0, foreword: str = default_foreword):
    async with session_maker() as session:
        async with session.begin():
            chat = Chat(chat_id=chat_id,
                        user_id=user_id,
                        role=role,
                        nickname=nickname,
                        foreword=foreword
                        )
            session.add(chat)
            
            
async def del_chat(chat_id: int, nickname: str, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            delete_nickname = (delete(Chat)
            .where(Chat.chat_id == chat_id)
            .where(Chat.nickname == nickname))
            await session.execute(delete_nickname)
            
async def get_nickname_id(nickname: str, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(select(Chat).where(Chat.nickname == nickname))
            nickname_id = result.first()
            return nickname_id