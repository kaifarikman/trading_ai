import os
from typing import List

from bot.services.openai_api import analyze_xauusd_screenshots
from asyncio import sleep
from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from bot.default_functions import send_message_aiogram_message, send_callback_aiogram_message
import bot.user.texts as texts
import bot.user.keyboards as keyboards
from bot.bot import bot
from config import ADMIN_PEER_ID

import db.crud.users as crud_users
from db.models import User

from bot.user.utils import check_last_datetime, is_authentication

router = Router()


@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    await state.clear()
    peer_id = message.from_user.id
    if not await crud_users.read_user(peer_id):
        user = User(
            peer_id=peer_id,
            ref_status=False,
            pressed_start=True,
            selected_learning=False,
            selected_signals=False
        )
        await crud_users.create_user(user)
    await send_message_aiogram_message(
        message=message,
        text=texts.start_text,
        keyboard=await keyboards.start_keyboard()
    )


@router.callback_query(F.data == 'start')
async def start_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await send_callback_aiogram_message(
        callback=callback,
        text=texts.start_text,
        keyboard=await keyboards.start_keyboard()
    )


@router.callback_query(F.data == 'join_team')
async def join_team_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.clear()

    peer_id = int(callback.from_user.id)
    if (await crud_users.read_user(peer_id)).ref_status:
        return await send_callback_aiogram_message(
            callback=callback,
            text=texts.already_registered,
            keyboard=await keyboards.back_keyboard()
        )

    await send_callback_aiogram_message(
        callback=callback,
        text=texts.exness_acc,
        keyboard=await keyboards.exness_acc()
    )


class TrainingPhotoState(StatesGroup):
    screenshot = State()


@router.callback_query(F.data.startswith('training_'))
async def training_choice_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()

    choice = callback.data.split('_')[-1]
    if choice == 'no':
        await send_callback_aiogram_message(
            callback=callback,
            text=texts.training_no,
            keyboard=await keyboards.back_keyboard(),
        )
    else:
        await callback.message.edit_reply_markup()
        await callback.message.answer_video(
            video='BAACAgIAAxkBAAMuaGedvNVAig-iybztDXkfmANBkOUAApVsAALFeUBLD8B-bTzxm8A2BA',
            # video='BAACAgIAAxkBAAIfxWhsLwoik6Xx1FrKJ801Q-6oLKkSAAKVbAACxXlAS7R4dbLR5AABLjYE',
            caption=texts.training_yes,
            reply_markup=await keyboards.back_keyboard(),
        )
    await state.set_state(TrainingPhotoState.screenshot)


@router.message(TrainingPhotoState.screenshot)
async def screenshot_message(message: Message, state: FSMContext):
    if not message.photo:
        return await send_message_aiogram_message(
            message=message,
            text=texts.screenshot_invalid,
            keyboard=await keyboards.back_keyboard()
        )
    await state.clear()
    peer_id = message.from_user.id
    message_id = message.photo[-1].file_id
    await bot.send_photo(
        chat_id=ADMIN_PEER_ID,
        photo=message_id,
        reply_markup=await keyboards.screenshot_to_admin(peer_id)
    )
    await send_message_aiogram_message(
        message=message,
        text='Ожидайте ответа',
        keyboard=await keyboards.back_keyboard()
    )


@router.callback_query(F.data == 'free_training')
@is_authentication
async def free_training_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await send_callback_aiogram_message(
        callback=callback,
        text=texts.materials_text,
        keyboard=await keyboards.back_keyboard()
    )


@router.callback_query(F.data == 'support')
async def support_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await send_callback_aiogram_message(
        callback=callback,
        text=texts.support_text,
        keyboard=await keyboards.back_keyboard()
    )


class WaitingScreenState(StatesGroup):
    screenshot = State()


@router.callback_query(F.data == "analysis_and_signal")
@is_authentication
async def analysis_and_signal_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await send_callback_aiogram_message(
        callback=callback,
        text=texts.start_chat
    )
    await state.set_state(WaitingScreenState.screenshot)


@router.message(WaitingScreenState.screenshot)
async def screenshot_message(message: Message, state: FSMContext, album: List[Message] = None):
    photos = []
    if message.photo:
        photo = message.photo[-1]
        file_id = photo.file_id
        file = await bot.get_file(file_id)
        file_path = file.file_path

        save_path = "bot/services/screenshots/photo.jpg"
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        await bot.download_file(file_path, save_path)
        photos.append(save_path)
    elif album is not None:
        for i in range(len(album)):
            element = album[i]
            if element.photo:
                file_id = element.photo[-1].file_id
                save_path = f"bot/services/screenshots/photo{i}.jpg"
                file = await bot.get_file(file_id)
                file_path = file.file_path
                os.makedirs(os.path.dirname(save_path), exist_ok=True)
                await bot.download_file(file_path, save_path)
                photos.append(save_path)

    if not photos:
        return await send_message_aiogram_message(
            message=message,
            text=texts.screenshot_invalid,
            keyboard=await keyboards.back_keyboard()
        )

    await state.clear()

    openai_answer = analyze_xauusd_screenshots(photos)
    for save_path in photos:
        if os.path.exists(save_path):
            os.remove(save_path)

    await send_message_aiogram_message(
        message=message,
        text=openai_answer,
        keyboard=await keyboards.back_keyboard(),
    )
