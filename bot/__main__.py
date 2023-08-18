import asyncio
import logging
import random
import sys
import os
from dotenv import load_dotenv

from aiogram import F, Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext

from structures import PharasesStates

load_dotenv()

# Bot token can be obtained via https://t.me/BotFather
TOKEN = os.getenv("token")

pre_phrase = ['Погоняло дня']

phrases = ['Веста', 'Разъяренная пизда', 'ВСУ', 'Вася Вест', 'Инвокер', 'Зверюга', 'Квася Вест Эскорт', 'Танкист вайф', 'Тремор Гёрл', 'Крейзи Фокс', 'Вибромод']

# All handlers should be attached to the Router (or Dispatcher)
router = Router()

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
    if command.args in phrases:
        phrases.remove(command.args)
        await message.answer(f'Удалили кликуху <b>"{command.args}"</b>')
    elif 0 <= int(command.args) < len(phrases):
        await message.answer(f'Удалили кликуху <b>"{phrases[int(command.args)]}"</b>')
        phrases.pop(int(command.args))
    # elif command.args not in phrases:
    #     print(type(int(command.args)), command.args)
    else:
        await message.answer('Погоди, погоди, после /delname нужно дописать кликуху или ее номер.\nИспользуйте /namelist для того чтобы увидеть список кликух.')


def random_phrase():
    return random.choice(phrases)


def add_pharase(phrase):
    phrases.append(phrase)
        

async def main() -> None:
    

    # Dispatcher is a root router
    dp = Dispatcher()   
    # ... and all other routers should be attached to Dispatcher
    dp.include_router(router)

    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot stopped!")