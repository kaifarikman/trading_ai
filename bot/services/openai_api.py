import base64
from openai import OpenAI
from config import OPENAI_API_KEY
from typing import List, Optional

client = OpenAI(api_key=OPENAI_API_KEY)


def analyze_xauusd_screenshots(image_paths: List[str]) -> Optional[str]:
    system_prompt = """Ты - профессиональный трейдер. Анализируй графики XAUUSD (15M и 1H) по:

    1. Тренд (▲▼➖) + MA50
    2. Уровни S/R (2+ теста)
    3. Точки входа (отскоки)

    Формат ответа:
    📊 XAUUSD Analysis
    ✅ Signal: [Long/Short/None]
    🎯 Entry: $XXXX.XX
    🛡 SL: $XXXX.XX
    💰 TP: $XXXX.XX
    📌 Confirmation: [Уровень/Паттерн]
    
    не отвечай объемно. лучше четко и структурированно
    """


    try:
        encoded_images = []
        for path in image_paths:
            with open(path, "rb") as img_file:
                encoded_images.append(
                    f"data:image/jpeg;base64,{base64.b64encode(img_file.read()).decode('utf-8')}"
                )

        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Проанализируй графики:"},
                        *[{"type": "image_url", "image_url": {"url": img}} for img in encoded_images]
                    ]
                }
            ],
            max_tokens=500,
            temperature=0.1
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Error: {str(e)}"
