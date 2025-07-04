from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def send_callback_aiogram_message(callback, text, keyboard=None):
    try:
        await callback.message.edit_text(text=text, reply_markup=keyboard)
    except:
        await callback.message.edit_reply_markup()
        await callback.message.answer(text=text, reply_markup=keyboard)


async def send_message_aiogram_message(message, text, keyboard=None):
    try:
        await message.edit_text(text=text, reply_markup=keyboard)
    except:
        await message.answer(text=text, reply_markup=keyboard)


def generate_keyboard(buttons_data, layout):
    buttons = []
    index = 0

    for row_size in layout:
        row = [
            InlineKeyboardButton(
                text=buttons_data[i][0], callback_data=buttons_data[i][1]
            )
            for i in range(index, index + row_size)
        ]
        buttons.append(row)
        index += row_size

    return InlineKeyboardMarkup(inline_keyboard=buttons)
