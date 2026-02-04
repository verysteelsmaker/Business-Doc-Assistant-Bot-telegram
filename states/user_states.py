from aiogram.fsm.state import State, StatesGroup

class BotStates(StatesGroup):
    waiting_for_documents = State() # Режим загрузки файлов
    chatting_with_docs = State()    # Режим вопросов по документам