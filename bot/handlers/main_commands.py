import asyncio
import random
from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.utils.markdown import hbold
from aiogram.filters import Command, CommandObject

from sqlalchemy.orm import sessionmaker

import aioschedule

from db import get_chat, set_chat
from middlewares import RegisterCheck


router = Router()
router.message.middleware(RegisterCheck())


@router.message(Command(commands=["dayname"]))
async def day_pharase(message: types.Message, session_maker: sessionmaker) -> None:
    nickname_list = await get_chat(message.chat.id, session_maker=session_maker)
    await message.answer(f'{nickname_list.foreword}: <b>{random.choice(nickname_list.nickname.limit(10))}</b>')
    
    
@router.message(Command(commands=["newname"]))
async def add_new_phrase(message: types.Message, command: CommandObject, session_maker: sessionmaker) -> None:
    if command.args:
        await message.answer(F'Новая кликуха <b>"{command.args}"</b>')
        await set_chat(message.chat.id, message.from_user.id, nickname=command.args, session_maker=session_maker) 
    else:
        await message.answer('Погоди, погоди, после /newname нужно дописать кликуху')  
    
    
@router.message(Command(commands=["setphrase"]))
async def set_phrase(message: types.Message, command: CommandObject) -> None:
    if command.args:
        await message.answer(F'Новое предисловие <b>"{command.args}"</b>')
    else:
        await message.answer('Погоди, погоди, после /setphrase нужно дописать предисловие')  


@router.message(Command(commands=["namelist"]))
async def get_name_list(message: types.Message) -> None:
    phrases_message = ''
    count = 0
    for phrase in phrases:
        phrase_msg = f'{count}: <b>{phrase}</b>'
        phrases_message += phrase_msg + '\n'
        count += 1
    await message.answer(phrases_message)
        
       
@router.message(Command(commands=["delname"]))
async def del_phrase(message: types.Message, command: CommandObject) -> None:
    user_msg = command.args
    
    if user_msg is None:
        await message.answer('Погоди, погоди, после /delname нужно дописать кликуху или ее номер.\nИспользуйте /namelist для того чтобы увидеть список кликух.')

    
    if user_msg in phrases:
        phrases.remove(user_msg)
        await message.answer(f'Кликуха <b>"{user_msg}"</b> удалена')
    elif user_msg.isnumeric():
        if 0 <= int(user_msg) < len(phrases):
            await message.answer(f'Кликуха <b>"{phrases[int(user_msg)]}"</b> удалена')
            phrases.pop(int(user_msg))
        else:
            await message.answer(f'Стопэ, фразы с таким номером не существует')
    else:
        await message.answer('Погоди, погоди, такой кликухи не существует.\nИспользуй /namelist для того чтобы увидеть список существующих кликух.')
   
   
async def scheduler():
    aioschedule.every().day.at("17:45").do(day_pharase)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)