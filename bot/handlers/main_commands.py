import random
from datetime import datetime, timedelta

from aiogram import Router, types
from aiogram.filters import Command, CommandObject
from sqlalchemy.orm import sessionmaker

from db import (
    del_chat,
    get_chat_items,
    get_last_msg,
    set_chat,
)
from middlewares import RegisterCheck


# scheduler = AsyncIOScheduler(timezone="Europe/Moscow")

router = Router()
router.message.middleware(RegisterCheck())
# router.message.middleware(SchedulerMiddleware(scheduler))


@router.message(Command(commands=["dayname"]))
async def day_pharase(
    message: types.Message, session_maker: sessionmaker
) -> None:
    datetime_3 = datetime.now()
    last_msg = await get_last_msg(message.chat.id, session_maker=session_maker)
    interval_list = await get_chat_interval(
        message.chat.id, session_maker=session_maker
    )
    interval = await parse_time(interval_list)
    interval_timedelta = timedelta(hours=interval[0], minutes=interval[1])
    nickname_list, foreword_list = await get_chat(
        message.chat.id, session_maker=session_maker
    )

    if len(nickname_list) < 1:
        await message.answer(
            'Необходимо добавить кликуху. Для этого воспользуйтесь командой\n/newname "название кликухи"'
        )
    elif len(foreword_list) < 1:
        await message.answer(
            'Необходимо добавить Предисловие. Для этого воспользуйтесь командой\n/setphrase "название предисловия"'
        )

    if last_msg[0] is None:
        await message.answer(
            f"{foreword_list[-1]}: {random.choice(nickname_list)}"
        )
        await set_chat(
            message.chat.id,
            message.from_user.id,
            session_maker=session_maker,
            message_datetime=datetime_3,
        )
    elif (last_msg[0] + interval_timedelta) > datetime_3:
        time_to_msg = (last_msg[0] + interval_timedelta) - datetime_3
        hours, minutes, seconds = convert_timedelta(time_to_msg)
        if hours >= 1:
            await message.answer(
                f"А уже все, узнать погоняло можно через:\n{hours} часа.\nДля изменения времени можно воспользоваться командой\n/setinterval"
            )
        elif minutes >= 1:
            await message.answer(
                f"А уже все, узнать погоняло можно через:\n{minutes} минут.\nДля изменения времени можно воспользоваться командой\n/setinterval"
            )
        else:
            await message.answer(
                f"А уже все, узнать погоняло можно через:\n{seconds} секунд.\nДля изменения времени можно воспользоваться командой\n/setinterval"
            )

    else:
        await message.answer(
            f"{foreword_list[-1]}: {random.choice(nickname_list)}"
        )
        await set_chat(
            message.chat.id,
            message.from_user.id,
            session_maker=session_maker,
            message_datetime=datetime_3,
        )


@router.message(Command(commands=["newname"]))
async def add_new_phrase(
    message: types.Message, command: CommandObject, session_maker: sessionmaker
) -> None:
    name_list = await get_chat(message.chat.id, session_maker=session_maker)

    if command.args is None:
        await message.answer(
            "Погоди, погоди, после /newname нужно дописать кликуху"
        )
    elif command.args in name_list[0]:
        await message.answer(f'Кликуха <b>"{command.args}"</b> уже существует')
    elif command.args not in name_list:
        await message.answer(f'Новая кликуха <b>"{command.args}"</b>')
        await set_chat(
            message.chat.id,
            message.from_user.id,
            nickname=command.args,
            session_maker=session_maker,
        )


@router.message(Command(commands=["setphrase"]))
async def set_phrase(
    message: types.Message, command: CommandObject, session_maker: sessionmaker
) -> None:
    if command.args:
        await message.answer(f'Новое предисловие <b>"{command.args}"</b>')
        await set_chat(
            message.chat.id,
            message.from_user.id,
            foreword=command.args,
            session_maker=session_maker,
        )
    else:
        await message.answer(
            "Погоди, погоди, после /setphrase нужно дописать предисловие"
        )


@router.message(Command(commands=["namelist"]))
async def get_name_list(
    message: types.Message, session_maker: sessionmaker
) -> None:
    nickname_list, foreword_list = await get_chat(
        message.chat.id, session_maker=session_maker
    )

    phrases_message = ""
    count = 0
    for phrase in nickname_list:
        phrase_msg = f"{count}: <b>{phrase}</b>"
        phrases_message += phrase_msg + "\n"
        count += 1
    await message.answer(phrases_message)


@router.message(Command(commands=["delname"]))
async def del_phrase(
    message: types.Message, command: CommandObject, session_maker: sessionmaker
) -> None:
    user_msg = command.args

    nickname_list, foreword_list = await get_chat(
        message.chat.id, session_maker=session_maker
    )

    if user_msg is None:
        await message.answer(
            "Погоди, погоди, после /delname нужно дописать кликуху или ее номер.\nИспользуйте /namelist для того чтобы увидеть список кликух."
        )

    if user_msg in nickname_list:
        await del_chat(
            chat_id=message.chat.id,
            nickname=user_msg,
            session_maker=session_maker,
        )
        await message.answer(f'Кликуха <b>"{user_msg}"</b> удалена')
    elif user_msg.isnumeric():
        if 0 <= int(user_msg) < len(nickname_list):
            await message.answer(
                f'Кликуха <b>"{nickname_list[int(user_msg)]}"</b> удалена'
            )
            await del_chat(
                chat_id=message.chat.id,
                nickname=nickname_list[int(user_msg)],
                session_maker=session_maker,
            )
        else:
            await message.answer("Стопэ, фразы с таким номером не существует")
    else:
        await message.answer(
            "Погоди, погоди, такой кликухи не существует.\nИспользуй /namelist для того чтобы увидеть список существующих кликух."
        )


@router.message(Command(commands=["setinterval"]))
async def set_time(
    message: types.Message, command: CommandObject, session_maker: sessionmaker
):
    if command.args is None:
        await message.answer(
            "Так, после /setinterval нужно дописать время в формате Час:Минута, например 8:00"
        )
    elif ":" not in command.args:
        await message.answer('Дубина, ты забыл поставить ":"')

    hours, minutes = command.args.split(":")
    if 0 <= int(hours) and 0 <= int(minutes) < 60:
        await set_chat(
            message.chat.id,
            message.from_user.id,
            session_maker=session_maker,
            interval=command.args,
        )
        await message.answer(
            f"Теперь через каждые {hours}ч и {minutes}м можно будет выбирать кликухи на день"
        )

    elif int(minutes) > 60:
        await message.answer("Минут не может быть больше 60")

    else:
        await message.answer(
            "Погоди, погоди, после /setinterval нужно дописать время в формате Час:Минута, например 8:00"
        )


async def get_chat(chat_id: int, session_maker: sessionmaker):
    items = await get_chat_items(chat_id=chat_id, session_maker=session_maker)
    nickname_list = []
    foreword_list = []

    for nickname in items:
        if nickname.nickname is not None:
            nickname_list.append(nickname.nickname)
        elif nickname.foreword is not None:
            foreword_list.append(nickname.foreword)
        else:
            pass

    return nickname_list, foreword_list


async def get_chat_interval(
    chat_id: int, session_maker: sessionmaker
) -> list[str]:
    items = await get_chat_items(chat_id=chat_id, session_maker=session_maker)
    interval_list = []
    for interval in items:
        if interval.interval is not None:
            interval_list.append(interval.interval)

    if len(interval_list) < 1:
        interval_list.append("24:00")

    return interval_list


async def parse_time(interval_list: list[str]) -> list[int, int]:
    hours, minutes = interval_list[0].split(":")
    return int(hours), int(minutes)


def convert_timedelta(duration):
    days, seconds = duration.days, duration.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    return hours, minutes, seconds
