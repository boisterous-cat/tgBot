from datetime import datetime

import pytest
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.enums import ChatType
from aiogram.methods import SendMessage
from aiogram.methods.base import TelegramType
from aiogram.types import (
    Update, Chat, User, Message, CallbackQuery,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from keyboards.keyboards import top_10, less_10


# Константы для этого набора тестов
user_id = 123456
callback_data_top = "top_10_pressed"
callback_data_tail = "less_10_pressed"


# Генерируем текстовое сообщение с инлайн кнопками
def make_top_incoming_message() -> Message:
    """
    Генерирует текстовое сообщение с командой /top от юзера к боту
    :return: объект Message с текстовой командой /top
    """
    return Message(
        message_id=1,
        chat=Chat(id=user_id, type=ChatType.PRIVATE),
        from_user=User(id=user_id, is_bot=False, first_name="User"),
        date=datetime.now(),
        text="/top"
    )


# Отправим первый коллбек боту
def make_top_incoming_callback() -> CallbackQuery:
    """
    Генерирует объект CallbackQuery,
    имитирующий результат нажатия юзером кнопки
    с callback_data "top_10_pressed"
    :return: объект CallbackQuery
    """
    return CallbackQuery(
        id="1111111111111",
        chat_instance="22222222222222",
        from_user=User(id=user_id, is_bot=False, first_name="User"),
        data=callback_data_top,
        message=Message(
            message_id=1,
            chat=Chat(id=user_id, type=ChatType.PRIVATE),
            from_user=User(id=user_id, is_bot=False, first_name="User"),
            date=datetime.now(),
            text="Топ 10 лучших"
        )
    )


# Отправим второй коллбек боту
def make_less_incoming_callback() -> CallbackQuery:
    """
    Генерирует объект CallbackQuery,
    имитирующий результат нажатия юзером кнопки
    с callback_data "less_10_pressed"
    :return: объект CallbackQuery
    """
    return CallbackQuery(
        id="1111111111100",
        chat_instance="22222222222200",
        from_user=User(id=user_id, is_bot=False, first_name="User"),
        data=callback_data_tail,
        message=Message(
            message_id=1,
            chat=Chat(id=user_id, type=ChatType.PRIVATE),
            from_user=User(id=user_id, is_bot=False, first_name="User"),
            date=datetime.now(),
            text="Топ 10 худших"
        )
    )


# Проверим что бот действительно отправил текстовое сообщение
# И есть инлайн кнопки
@pytest.mark.asyncio
async def test_top_command(dp, bot):
    # Создаём ответное сообщение от Telegram в ответ на команду /top
    bot.add_result_for(
        method=SendMessage,
        ok=True,
        # result сейчас не нужен
    )

    # Отправляем сообщение с командой /top
    update = await dp.feed_update(
        bot,
        Update(message=make_top_incoming_message(), update_id=1)
    )

    # Убеждаемся, что сообщение обработано
    assert update is not UNHANDLED

    # Получаем отправленное ботом сообщение
    outgoing_message: TelegramType = bot.get_request()
    # Проверяем содержимое: тип, текст, наличие клавиатуры, содержимое клавиатуры
    assert isinstance(outgoing_message, SendMessage)
    assert outgoing_message.text == "Выберите какие города показать"
    assert outgoing_message.reply_markup is not None
    markup = outgoing_message.reply_markup
    assert isinstance(markup, InlineKeyboardMarkup)
    button_top: InlineKeyboardButton = markup.inline_keyboard[0][0]
    assert button_top == top_10
    button_tail: InlineKeyboardButton = markup.inline_keyboard[1][0]
    assert button_tail == less_10


# Убедимся что бот верно отвечает на наши кнопки
@pytest.mark.asyncio
async def test_top_10_pressed_callback(dp, bot):
    # Создаём ответное сообщение от Telegram при ответе на колбэк
    bot.add_result_for(
        method=SendMessage,
        ok=True
    )

    # Отправляем коллбэк с data = myid
    update = await dp.feed_update(
        bot,
        Update(callback_query=make_top_incoming_callback(), update_id=1)
    )

    # Убеждаемся, что коллбэк обработан
    assert update is not UNHANDLED

    # Получаем отправленный ботом коллбэк
    outgoing_callback: TelegramType = bot.get_request()

    # Проверяем содержимое: тип, текст, вид алерта
    assert isinstance(outgoing_callback, SendMessage)
    assert "Топ 10 лучших" in outgoing_callback.text
    assert outgoing_callback.parse_mode == 'HTML'


@pytest.mark.asyncio
async def test_less_10_pressed_callback(dp, bot):
    # Создаём ответное сообщение от Telegram при ответе на колбэк
    bot.add_result_for(
        method=SendMessage,
        ok=True
    )

    # Отправляем коллбэк с data = myid
    update = await dp.feed_update(
        bot,
        Update(callback_query=make_less_incoming_callback(), update_id=1)
    )

    # Убеждаемся, что коллбэк обработан
    assert update is not UNHANDLED

    # Получаем отправленный ботом коллбэк
    outgoing_callback: TelegramType = bot.get_request()

    # Проверяем содержимое: тип, текст, вид алерта
    assert isinstance(outgoing_callback, SendMessage)
    assert "Топ 10 худших" in outgoing_callback.text
    assert outgoing_callback.parse_mode == 'HTML'

# @pytest.mark.asyncio
# async def test_process_help_command():
#     message = AsyncMock()
#     await process_help_command(message)
#
#     message.answer.assert_called_with(text=LEXICON_RU['/help'])
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
