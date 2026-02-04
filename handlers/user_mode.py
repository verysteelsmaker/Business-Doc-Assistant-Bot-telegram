import os
from aiogram import Router, F, types, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from keyboards import builders as kb
from states.user_states import BotStates
# ОБНОВЛЕННЫЙ ИМПОРТ:
from services.vector_store import add_document_to_index, get_relevant_context, clear_user_memory
from services.llm_client import get_answer_from_docs

router = Router()

@router.message(CommandStart())
async def start_handler(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Добрый день. Я ваш цифровой ассистент.\n"
        "Я умею анализировать корпоративные документы (PDF, Word, Excel, TXT) "
        "и отвечать на вопросы строго по их содержанию.\n\n"
        "Пожалуйста, выберите действие в меню ниже.",
        reply_markup=kb.main_menu_kb()
    )

@router.message(F.text == "📂 Загрузить документы")
async def start_upload(message: types.Message, state: FSMContext):
    await state.set_state(BotStates.waiting_for_documents)
    await message.answer(
        "Перешел в режим загрузки. Отправьте файлы (PDF, DOCX, CSV, TXT).\n"
        "Вы можете отправлять их по одному или выделить несколько сразу.\n"
        "По завершении нажмите 'Завершить загрузку'.",
        reply_markup=kb.stop_upload_kb()
    )

# ОБНОВЛЕННЫЙ ХЕНДЛЕР ДОКУМЕНТОВ
@router.message(BotStates.waiting_for_documents, F.document)
async def handle_document(message: types.Message, bot: Bot):
    file_id = message.document.file_id
    file_name = message.document.file_name
    
    # Скачиваем файл
    file = await bot.get_file(file_id)
    file_path = file.file_path
    
    # Сохраняем временно с оригинальным расширением
    temp_filename = f"temp_{message.from_user.id}_{file_name}"
    
    msg = await message.answer(f"⏳ Получен файл: {file_name}. Обработка...")
    
    try:
        await bot.download_file(file_path, temp_filename)
        
        # Вызываем универсальную функцию добавления
        chunks_count = add_document_to_index(temp_filename, message.from_user.id)
        
        # Удаляем файл после обработки
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
            
        await msg.edit_text(f"✅ Файл '{file_name}' успешно проиндексирован. Фрагментов: {chunks_count}.")
        
    except Exception as e:
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
        await msg.edit_text(f"❌ Ошибка при чтении файла '{file_name}':\n{str(e)}")

@router.message(BotStates.waiting_for_documents, F.text == "✅ Завершить загрузку")
async def finish_upload(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Загрузка завершена. База знаний обновлена.\n"
        "Теперь вы можете задать вопрос по загруженным материалам.",
        reply_markup=kb.main_menu_kb()
    )

@router.message(F.text == "💬 Задать вопрос")
async def ask_question_mode(message: types.Message, state: FSMContext):
    await state.set_state(BotStates.chatting_with_docs)
    await message.answer(
        "Я готов отвечать. Сформулируйте ваш запрос по документам.",
        reply_markup=kb.back_kb()
    )

@router.message(BotStates.chatting_with_docs, F.text)
async def process_question(message: types.Message):
    if message.text == "🔙 В главное меню":
        return
        
    waiting_msg = await message.answer("⏳ Анализирую информацию...")
    
    context = get_relevant_context(message.text, message.from_user.id)
    
    if not context:
        await waiting_msg.edit_text("К сожалению, в загруженных документах не найдено информации по вашему запросу.")
        return

    answer = await get_answer_from_docs(message.text, context)
    
    await waiting_msg.delete()
    await message.answer(answer, parse_mode="Markdown")

@router.message(F.text == "🔙 В главное меню")
async def back_to_main(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Главное меню.", reply_markup=kb.main_menu_kb())

@router.message(F.text == "🧹 Очистить базу знаний")
async def clear_db(message: types.Message):
    clear_user_memory(message.from_user.id)
    await message.answer(
        "Контекст очищен (имитация). Вы можете загрузить новые данные.",
        reply_markup=kb.main_menu_kb()
    )