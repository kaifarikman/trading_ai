from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from bot.default_functions import send_message_aiogram_message, send_callback_aiogram_message
from config import ADMIN_PEER_ID
import bot.admin.texts as texts
import bot.admin.keyboards as keyboards
from bot.bot import bot

import db.crud.users as crud_users

router = Router()


@router.message(Command('admin'))
async def admin_command(message: Message, state: FSMContext):
    await state.clear()
    if int(message.from_user.id) != int(ADMIN_PEER_ID):
        return await send_message_aiogram_message(
            message=message,
            text=texts.invalid_admin,
        )
    await send_message_aiogram_message(
        message=message,
        text=texts.admin_text,
        keyboard=await keyboards.admin_keyboard()
    )


@router.callback_query(F.data == 'admin')
async def admin_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await send_callback_aiogram_message(
        callback=callback,
        text=texts.admin_text,
        keyboard=await keyboards.admin_keyboard()
    )


@router.callback_query(F.data.startswith('screenshot_user_'))
async def screenshot_user_callback_choice(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()

    choice, peer_id = callback.data.split('_')[-2:]
    if choice == 'accept':
        text = texts.accept_screenshot
        await crud_users.change_user_status(int(peer_id), True)
    else:
        text = texts.reject_screenshot
        await crud_users.change_user_status(int(peer_id), False)

    await bot.send_message(
        chat_id=peer_id,
        text=text,
        reply_markup=await keyboards.user_back_keyboard()
    )
    await send_callback_aiogram_message(
        callback=callback,
        text=texts.admin_answer_for_screenshot,
        keyboard=await keyboards.back_keyboard()
    )


class AdminState(StatesGroup):
    send = State()


@router.callback_query(F.data == 'admin_mailing')
async def admin_mailing_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()

    await send_callback_aiogram_message(
        callback=callback,
        text=texts.mailing_test,
        keyboard=await keyboards.back_keyboard(),
    )
    await state.set_state(AdminState.send)


@router.message(AdminState.send)
async def send_post(message: Message, state: FSMContext):
    users = await crud_users.get_users()
    count = 0
    for user_id in users:
        try:
            await message.copy_to(user_id)
            count += 1
        except Exception as e:
            print(e)
    await message.answer(
        text=f"{count} пользователей получило рассылку.",
        reply_markup=await keyboards.back_keyboard()
    )
    await state.clear()
