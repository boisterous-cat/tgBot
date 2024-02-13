from datetime import datetime

import pytest
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.enums import ChatType
from aiogram.methods import SendMessage
from aiogram.methods.base import TelegramType
from aiogram.types import (
    Update, Chat, User, Message, InlineKeyboardMarkup,InlineKeyboardButton
)

import keyboards.keyboards
from lexicon.lexicon_ru import LEXICON_RU
from keyboards.keyboards import user_button, github_button


@pytest.mark.asyncio
async def test_start_command(dp, bot):
    bot.add_result_for(
        method=SendMessage,
        ok=True,
        # result сейчас можно пропустить
    )
    chat = Chat(id=1234567, type=ChatType.PRIVATE)
    user = User(id=1234567, is_bot=False, first_name="User")
    # Создаём фейковое входящее сообщение
    message = Message(
        message_id=1,
        chat=chat,
        from_user=user,
        text="/start",
        date=datetime.now()
    )
    # "Скармливаем" созданное сообщение
    result = await dp.feed_update(
        bot,
        Update(message=message, update_id=1)
    )
    # Если диспетчер не смог найти хэндлер для созданного сообщения,
    # то от вызова feed_update(...) вернётся UNHANDLED
    assert result is not UNHANDLED
    # Получаем сообщение, которое отправил наш бот
    outgoing_message: TelegramType = bot.get_request()
    # Проверяем, что сообщение было передано методом send_message
    assert isinstance(outgoing_message, SendMessage)
    assert outgoing_message.text == LEXICON_RU['/start']

@pytest.mark.asyncio
async def test_help_command(dp, bot):
    bot.add_result_for(
        method=SendMessage,
        ok=True,
    )
    chat = Chat(id=1234567, type=ChatType.PRIVATE)
    user = User(id=1234567, is_bot=False, first_name="User")
    # Создаём фейковое входящее сообщение
    message = Message(
        message_id=1,
        chat=chat,
        from_user=user,
        text="/help",
        date=datetime.now()
    )
    # "Скармливаем" созданное сообщение
    result = await dp.feed_update(
        bot,
        Update(message=message, update_id=1)
    )
    # Если диспетчер не смог найти хэндлер для созданного сообщения,
    # то от вызова feed_update(...) вернётся UNHANDLED
    assert result is not UNHANDLED
    # Получаем сообщение, которое отправил наш бот
    outgoing_message: TelegramType = bot.get_request()
    # Проверяем, что сообщение было передано методом send_message
    assert isinstance(outgoing_message, SendMessage)
    assert outgoing_message.text == LEXICON_RU['/help']

@pytest.mark.asyncio
async def test_project_command(dp, bot):
    bot.add_result_for(
        method=SendMessage,
        ok=True,
    )
    chat = Chat(id=1234567, type=ChatType.PRIVATE)
    user = User(id=1234567, is_bot=False, first_name="User")
    # Создаём фейковое входящее сообщение
    message = Message(
        message_id=1,
        chat=chat,
        from_user=user,
        text="/project",
        date=datetime.now()
    )
    # "Скармливаем" созданное сообщение
    result = await dp.feed_update(
        bot,
        Update(message=message, update_id=1)
    )
    # Если диспетчер не смог найти хэндлер для созданного сообщения,
    # то от вызова feed_update(...) вернётся UNHANDLED
    assert result is not UNHANDLED
    # Получаем сообщение, которое отправил наш бот
    outgoing_message: TelegramType = bot.get_request()
    # Проверяем, что сообщение было передано методом send_message
    assert isinstance(outgoing_message, SendMessage)
    assert "Перейти на страницу проекта" in outgoing_message.text
    assert outgoing_message.reply_markup is not None
    markup = outgoing_message.reply_markup
    assert isinstance(markup, InlineKeyboardMarkup)
    button_git: InlineKeyboardButton = markup.inline_keyboard[0][0]
    assert button_git == github_button
    button_me: InlineKeyboardButton = markup.inline_keyboard[1][0]
    assert button_me == user_button
#
# @pytest.mark.asyncio
# async def test_process_project_command():
#     message = AsyncMock()
#     await process_project_command(message)
#     message.answer.assert_called_with(text='Перейти на страницу проекта в gitHub или связаться с автором🤔',
#         reply_markup=keyboard)
#
# @pytest.mark.asyncio
# async def test_process_top_command():
#     requester = MockedBot(request_handler=MessageHandler(process_top_command, Command(commands=["top"])))
#     requester.add_result_for(SendMessage, ok=True)
#     calls = await requester.query(MESSAGE.as_object(text="/top"))
#     answer_message = calls.send_message.fetchone()
#     reply_keyboard_markup_dict = answer_message.reply_markup
#
#     assert answer_message.text == "Выберите какие города показать"
#     assert isinstance(reply_keyboard_markup_dict, dict)
#
# @pytest.mark.asyncio
# async def test_process_aqi_command():
#     requester = MockedBot(request_handler=MessageHandler(process_aqi_command, Command(commands=["aqi"]), state=default_state))
#     requester.add_result_for(SendMessage, ok=True)
#     calls = await requester.query(MESSAGE.as_object(text="/aqi"))
#     answer_message = calls.send_message.fetchone().text
#     assert answer_message == "Пожалуйста, введите уровень CO"
#     #assert calls.__getstate__()==FSMFillForm.fill_co
#
# #@pytest.mark.parametrize("case", [F.about["test"], F.about[100]])
# @pytest.mark.asyncio
# async def test_process_top_10_press():
#     requester = MockedBot(CallbackQueryHandler(process_top_10_press, F.data=='top_10_pressed'))
#
#     callback_query = CALLBACK_QUERY.as_object(
#         data='top_10_pressed', message=MESSAGE.as_object(text="")
#     )
#     calls = await requester.query(callback_query)
#
#     answer_text = calls.send_message.fetchone()
#     assert "Топ 10 лучших городов" in answer_text.text
#     assert answer_text.parse_mode=='HTML'
#     assert F.data == 'top_100_pressed'
#
#     # callback_query = CALLBACK_QUERY.as_object(
#     #     data='top_10_pressed', message=MESSAGE.as_object(text="Hello world!")
#     # )
#     # calls = await requester.query(callback_query)
#     #
#     # answer_text = calls.send_message.fetchone().text
#     # assert answer_text == "Hello, Mike"
