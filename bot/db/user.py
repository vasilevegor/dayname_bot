import datetime

from sqlalchemy import DATE, BigInteger, String, select
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker

from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, unique=True, nullable=False
    )

    username: Mapped[str] = mapped_column(
        String(32), unique=False, nullable=True
    )

    reg_date: Mapped[datetime.datetime] = mapped_column(
        DATE, default=datetime.date.today()
    )

    def __str__(self):
        return f"<User:{self.user_id}>"

    def __repr__(self):
        return self.__str__()


async def get_user(user_id: int, session_maker: sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            user = await session.execute(
                select(User)
                .where(User.user_id == user_id)
                .order_by(User.user_id.desc())
            )
            return user
