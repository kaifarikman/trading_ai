from bot.default_functions import generate_keyboard


async def admin_keyboard():
    buttons = [
        ('Рассылка', 'admin_mailing')
    ]
    layout = [1]
    return generate_keyboard(buttons, layout)


async def back_keyboard():
    buttons = [
        ('Выйти в меню', 'admin')
    ]
    layout = [1]
    return generate_keyboard(buttons, layout)


async def user_back_keyboard():
    buttons = [
        ('Выйти в меню', 'start')
    ]
    layout = [1]
    return generate_keyboard(buttons, layout)