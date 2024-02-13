from unittest.mock import AsyncMock, patch

from aiogram.fsm.context import FSMContext
from aiogram import F
from keyboards.keyboards import keyboard, df_show_keyboard
import pytest
from aiogram.filters import Command, StateFilter
from aiogram.methods import SendMessage
from handlers.user_handlers import process_start_command
from handlers.user_handlers import process_top_command
from handlers.user_handlers import process_help_command,process_project_command
from handlers.user_handlers import process_top_10_press
from lexicon.lexicon_ru import LEXICON_RU
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram_tests import MockedBot
from aiogram_tests.handler import CallbackQueryHandler
from aiogram_tests.handler import MessageHandler
from aiogram_tests.types.dataset import CALLBACK_QUERY
from aiogram_tests.types.dataset import MESSAGE
from handlers.user_handlers import FSMFillForm
from handlers.user_handlers import process_aqi_command
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.memory import MemoryStorage

@pytest.fixture()
def state(bot: MockedBot):
    storage = MemoryStorage()
    key = StorageKey(user_id=42, chat_id=-42, bot_id=bot.id)
    ctx = storage.storage[key]
    ctx.state = "test"
    ctx.data = {"foo": "bar"}
    return FSMContext(storage=storage, key=key)


@pytest.mark.asyncio
async def test_start_handler():
    message = AsyncMock()
    await process_start_command(message)

    message.answer.assert_called_with(text=LEXICON_RU['/start'])

@pytest.mark.asyncio
async def test_process_help_command():
    message = AsyncMock()
    await process_help_command(message)

    message.answer.assert_called_with(text=LEXICON_RU['/help'])

@pytest.mark.asyncio
async def test_process_project_command():
    message = AsyncMock()
    await process_project_command(message)
    message.answer.assert_called_with(text='Перейти на страницу проекта в gitHub или связаться с автором🤔',
        reply_markup=keyboard)

@pytest.mark.asyncio
async def test_process_top_command():
    requester = MockedBot(request_handler=MessageHandler(process_top_command, Command(commands=["top"])))
    requester.add_result_for(SendMessage, ok=True)
    calls = await requester.query(MESSAGE.as_object(text="/top"))
    answer_message = calls.send_message.fetchone()
    reply_keyboard_markup_dict = answer_message.reply_markup

    assert answer_message.text == "Выберите какие города показать"
    assert isinstance(reply_keyboard_markup_dict, dict)

@pytest.mark.asyncio
async def test_process_aqi_command():
    requester = MockedBot(request_handler=MessageHandler(process_aqi_command, Command(commands=["aqi"]), state=default_state))
    requester.add_result_for(SendMessage, ok=True)
    calls = await requester.query(MESSAGE.as_object(text="/aqi"))
    answer_message = calls.send_message.fetchone().text
    assert answer_message == "Пожалуйста, введите уровень CO"
    #assert calls.__getstate__()==FSMFillForm.fill_co

#@pytest.mark.parametrize("case", [F.about["test"], F.about[100]])
@pytest.mark.asyncio
async def test_process_top_10_press():
    requester = MockedBot(CallbackQueryHandler(process_top_10_press, F.data=='top_10_pressed'))

    callback_query = CALLBACK_QUERY.as_object(
        data='top_10_pressed', message=MESSAGE.as_object(text="")
    )
    calls = await requester.query(callback_query)

    answer_text = calls.send_message.fetchone()
    assert "Топ 10 лучших городов" in answer_text.text
    assert answer_text.parse_mode=='HTML'
    assert F.data == 'top_100_pressed'

    # callback_query = CALLBACK_QUERY.as_object(
    #     data='top_10_pressed', message=MESSAGE.as_object(text="Hello world!")
    # )
    # calls = await requester.query(callback_query)
    #
    # answer_text = calls.send_message.fetchone().text
    # assert answer_text == "Hello, Mike"