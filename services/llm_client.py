import os
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

MODEL_NAME = os.getenv("MODEL_NAME", "deepseek/deepseek-r1:free")

async def get_answer_from_docs(query: str, context: str) -> str:
    """Генерация ответа строго по контексту."""
    
    system_prompt = (
        "Вы — строгий деловой ассистент. Ваша задача — отвечать на вопросы пользователя "
        "ИСКЛЮЧИТЕЛЬНО на основе предоставленного ниже контекста из документов.\n"
        "1. Не добавляйте информацию от себя.\n"
        "2. Если ответа нет в контексте, ответьте: 'К сожалению, в предоставленных документах нет информации по вашему вопросу'.\n"
        "3. Стиль общения: официально-деловой, лаконичный.\n"
        "4. Цитируйте пункты документов, если это уместно.\n\n"
        f"КОНТЕКСТ:\n{context}"
    )

    try:
        response = await client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query},
            ],
            temperature=0.1, # Низкая температура для минимизации галлюцинаций
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Произошла ошибка при обращении к нейросети: {e}"