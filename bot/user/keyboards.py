from bot.default_functions import generate_keyboard


async def start_keyboard():
    buttons = [
        ('📚 Бесплатное обучение', 'free_training'),
        ('📈 Анализ и сигнал', 'analysis_and_signal'),
        ('💬 Поддержка', 'support')
    ]
    layout = [1, 1, 1]
    return generate_keyboard(buttons, layout)


async def exness_acc():
    buttons = [
        ('Да, у меня уже есть аккаунт', 'training_yes'),
        ('Нет, у меня нет аккаунта', 'training_no'),
        ('Выйти в главное меню', 'start')
    ]
    layout = [1, 1, 1]
    return generate_keyboard(buttons, layout)


async def back_keyboard():
    buttons = [
        ('Выйти в главное меню', 'start')
    ]
    layout = [1]
    return generate_keyboard(buttons, layout)


async def screenshot_to_admin(peer_id):
    buttons = [
        ('Принять', f'screenshot_user_accept_{peer_id}'),
        ('Отклонить', f'screenshot_user_reject_{peer_id}'),
    ]
    layout = [1, 1]
    return generate_keyboard(buttons, layout)


async def exness_group():
    buttons = [
        ('Попасть в команду', 'free_training'),
        ('Выйти в главное меню', 'start')
    ]
    layout = [1, 1]
    return generate_keyboard(buttons, layout)
