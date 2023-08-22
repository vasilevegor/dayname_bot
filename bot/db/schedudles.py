from sqlalchemy import BigInteger, String, select
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker

from .base import BaseModel


class Scheduler(BaseModel):
    __tablename__ = "schedulers"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, unique=True, nullable=False
    )

    chat_id: Mapped[int] = mapped_column(
        BigInteger, unique=False, nullable=False
    )

    time: Mapped[str] = mapped_column(String(32), unique=False, nullable=False)

    def __str__(self):
        return f"<User:{self.user_id}>"

    def __repr__(self):
        return self.__str__()


async def get_time_chat(chat_id: int, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            scheduler = await session.execute(
                select(Scheduler)
                .where(Scheduler.chat_id == chat_id)
                .order_by(Scheduler.chat_id.desc())
            )
            return scheduler


async def set_time_chat(chat_id: int, time: str, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            scheduler = Scheduler(chat_id=chat_id, time=time)
            session.add(scheduler)


async def set_schedudle_msg(session_maker: sessionmaker) -> None:
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(Scheduler).order_by(Scheduler.id.desc())
            )
            schedul_list = []
            for time in result.scalars():
                hours, minutes = time.time.split(":")
                chat_id = time.chat_id
                schedul_list.append([chat_id, hours, minutes])

            return schedul_list
