import asyncio
import random
from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.utils.markdown import hbold
from aiogram.filters import Command, CommandObject

import aioschedule

from db import get_chat, set_chat


router = Router()

pre_phrase = ['Погоняло дня']

phrases = ['Веста', 'Разъяренная пизда', 'ВСУ', 'Вася Вест', 'Инвокер', 'Зверюга', 'Квася Вест Эскорт', 'Танкист вайф', 'Тремор Гёрл', 'Крейзи Фокс', 'Вибромод']

@router.message(Command(commands=["dayname"]))
async def day_pharase(message: types.Message) -> None:
    await message.answer(f'{pre_phrase[-1]}: <b>{random_phrase()}</b>')
    
    
@router.message(Command(commands=["newname"]))
async def add_new_phrase(message: types.Message, command: CommandObject) -> None:
    if command.args:
        await message.answer(F'Новая кликуха <b>"{command.args}"</b>')
        add_pharase(command.args) 
    else:
        await message.answer('Погоди, погоди, после /newname нужно дописать кликуху')  
    
    
@router.message(Command(commands=["setphrase"]))
async def set_phrase(message: types.Message, command: CommandObject) -> None:
    if command.args:
        pre_phrase.append(command.args)
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


def random_phrase(chat_id: int):
    phrases = get_chat(chat_id)
    return random.choice(phrases)


def add_pharase(chat_id: int, user_id: int, role: int = 0, nickname: str, foreword: str = pre_phrase):
    set_chat(chat_id, user_id, role, nickname, foreword)
   
   
async def scheduler():
    aioschedule.every().day.at("17:45").do(day_pharase)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)