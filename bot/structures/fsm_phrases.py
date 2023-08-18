from aiogram.fsm.state import StatesGroup, State


class PharasesStates(StatesGroup):
    waiting_new_phrase = State()
    waiting_for_new_pre_phrase = State()
