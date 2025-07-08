from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import db.crud.users as crud_users
from bot.default_functions import send_message_aiogram_message, send_callback_aiogram_message
import bot.user.texts as texts
import bot.user.keyboards as keyboards


def is_authentication(func):
    async def wrapper(message: Message | CallbackQuery, state: FSMContext):
        peer_id = int(message.from_user.id)
        status = await crud_users.read_user(peer_id)
        if not status.ref_status:
            if isinstance(message, Message):
                return await send_message_aiogram_message(
                    message=message,
                    text=texts.no_access_to_exness,
                    keyboard=await keyboards.no_access_to_exness()
                )
            return await send_callback_aiogram_message(
                callback=message,
                text=texts.no_access_to_exness,
                keyboard=await keyboards.no_access_to_exness()
            )
        else:
            return await func(message, state)

    return wrapper


def check_last_datetime(func):
    async def wrapper(message: Message | CallbackQuery, state: FSMContext):
        user_id = message.from_user.id
        return await func(message, state)

    return wrapper
