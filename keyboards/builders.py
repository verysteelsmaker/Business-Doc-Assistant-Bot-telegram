from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu_kb():
    kb = [
        [KeyboardButton(text="📂 Загрузить документы"), KeyboardButton(text="💬 Задать вопрос")],
        [KeyboardButton(text="🧹 Очистить базу знаний")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, input_field_placeholder="Выберите действие...")

def stop_upload_kb():
    kb = [[KeyboardButton(text="✅ Завершить загрузку")]]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def back_kb():
    kb = [[KeyboardButton(text="🔙 В главное меню")]]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)