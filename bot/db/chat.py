from datetime import datetime

from sqlalchemy import (
    BigInteger,
    DateTime,
    ForeignKey,
    Integer,
    String,
    delete,
    select,
)
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker

from .base import BaseModel


default_foreword = "Погоняло дня"


class Chat(BaseModel):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, unique=True, nullable=False
    )

    chat_id: Mapped[int] = mapped_column(
        BigInteger, unique=False, nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.user_id"), unique=False, nullable=False
    )

    role: Mapped[int] = mapped_column(
        Integer, default=0, unique=False, nullable=False
    )

    nickname: Mapped[str] = mapped_column(
        String(32), unique=False, nullable=True
    )

    foreword: Mapped[str] = mapped_column(
        String(32), unique=False, nullable=True
    )

    message_datetime: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), unique=False, nullable=True
    )

    interval: Mapped[str] = mapped_column(
        String(32), unique=False, nullable=True
    )

    def __str__(self):
        return f"<User:{self.user_id}>"

    def __repr__(self):
        return self.__str__()


async def get_chat_items(chat_id: int, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(Chat)
                .where(Chat.chat_id == chat_id)
                .order_by(Chat.id.desc())
            )

            return result.scalars()


async def get_time_id(chat_id: int, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            id_with_time = await session.execute(
                select(Chat.id)
                .where(Chat.message_datetime != None)
                .where(Chat.chat_id == chat_id)
                .order_by(Chat.id.desc())
            )

            last_id = await session.execute(
                select(Chat.id)
                .where(Chat.chat_id == chat_id)
                .order_by(Chat.id.desc())
            )

            return id_with_time.scalars(), last_id.scalars()


async def set_chat(
    chat_id: int,
    user_id: int,
    session_maker: sessionmaker,
    message_datetime: datetime = None,
    nickname: str = None,
    role: int = 0,
    foreword: str = None,
    interval: str = None,
):
    async with session_maker() as session:
        async with session.begin():
            chat = Chat(
                chat_id=chat_id,
                user_id=user_id,
                role=role,
                nickname=nickname,
                foreword=foreword,
                message_datetime=message_datetime,
                interval=interval,
            )
            session.add(chat)


async def del_chat(chat_id: int, nickname: str, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            delete_nickname = (
                delete(Chat)
                .where(Chat.chat_id == chat_id)
                .where(Chat.nickname == nickname)
            )
            await session.execute(delete_nickname)


async def get_nickname_id(nickname: str, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(Chat).where(Chat.nickname == nickname)
            )
            nickname_id = result.first()
            return nickname_id


async def get_last_msg(chat_id: int, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            last_msg = await session.execute(
                select(Chat.message_datetime)
                .where(Chat.chat_id == chat_id)
                .order_by(Chat.id.desc())
            )

            last_msg_list = []
            for msg in last_msg.scalars():
                if msg is not None:
                    last_msg_list.append(msg)
            return last_msg_list
