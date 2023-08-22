from typing import Any, Awaitable, Callable, Dict, Union

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select

from db import Chat, User


class RegisterCheck(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any],
    ) -> Any:
        session_maker = data["session_maker"]
        async with session_maker() as session:
            async with session.begin():
                user_result = await session.execute(
                    select(User).where(User.user_id == event.from_user.id)
                )
                chat_result = await session.execute(
                    select(Chat).where(Chat.user_id == event.from_user.id)
                )

                user: User = user_result.one_or_none()
                chat: Chat = chat_result.first()

                if user is not None:
                    pass

                user = User(
                    user_id=event.from_user.id,
                    username=event.from_user.username,
                )

                await session.merge(user)

                if chat is not None:
                    pass
                else:
                    chat = Chat(
                        chat_id=event.chat.id, user_id=event.from_user.id
                    )
                    await session.merge(chat)

        return await handler(event, data)
