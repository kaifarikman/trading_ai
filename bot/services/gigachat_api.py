from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
from config import token
from requests import request


def get_query_to_gigachat():
    with GigaChat(credentials=token, verify_ssl_certs=False, model="GigaChat-Pro", ) as giga:
        file = giga.upload_file(open("bot/services/screenshots/photo.jpg", "rb"))
        file_id = file.id_
        question = """«Ты профессиональный трейдер-аналитик. Проанализируй присланный скриншот графика XAUUSD (таймфрейм 15M или 1H). Определи, куда сейчас лучше заходить — в лонг или в шорт.
Дай чёткий ответ в формате:
1️⃣ Рекомендация: Лонг или Шорт.
2️⃣ Уровень входа.
3️⃣ Стоп-лосс.
4️⃣ Тейк-профит.
⚠️ Добавь дисклеймер: “Не является финансовой рекомендацией.”»"""
        payload = Chat(
            messages=[
                Messages(
                    role=MessagesRole.SYSTEM,
                    content=question,
                    attachments=[file_id]
                )
            ],
            temperature=0.1
        )
        response = giga.chat(payload)
        url = f"https://gigachat.devices.sberbank.ru/api/v1/files/{file_id}/delete"
        payload = {}
        headers = {
            'Accept': 'application/json',
            'Authorization': token
        }
        request("POST", url, headers=headers, data=payload)
        return response.choices[0].message.content
