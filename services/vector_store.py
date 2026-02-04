import os
# Импортируем загрузчики для разных форматов
from langchain_community.document_loaders import (
    PyPDFLoader, 
    Docx2txtLoader, 
    TextLoader, 
    CSVLoader,
    UnstructuredHTMLLoader
)
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

PERSIST_DIRECTORY = "./chroma_db"

embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def get_loader_by_extension(file_path: str):
    """Выбирает подходящий загрузчик на основе расширения файла."""
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()

    if ext == ".pdf":
        return PyPDFLoader(file_path)
    elif ext == ".docx":
        return Docx2txtLoader(file_path)
    elif ext == ".csv":
        # csv_args позволяет корректно читать разделители
        return CSVLoader(file_path, encoding='utf-8', csv_args={'delimiter': ','})
    elif ext in [".html", ".htm"]:
        return UnstructuredHTMLLoader(file_path)
    elif ext in [".txt", ".md", ".py", ".json", ".ini", ".log"]:
        # Для текстовых файлов используем TextLoader с utf-8
        return TextLoader(file_path, encoding='utf-8')
    else:
        # Пытаемся прочитать как текст, если формат неизвестен
        return TextLoader(file_path, encoding='utf-8')

def add_document_to_index(file_path: str, user_id: int):
    """Считывает файл любого поддерживаемого формата и добавляет в базу."""
    try:
        loader = get_loader_by_extension(file_path)
        documents = loader.load()
    except Exception as e:
        raise ValueError(f"Ошибка при чтении файла (возможно, формат не поддерживается или кодировка не UTF-8): {e}")

    # Разбиваем текст на чанки
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(documents)

    if not chunks:
        return 0

    # Добавляем метаданные
    for chunk in chunks:
        chunk.metadata["user_id"] = str(user_id)
        # Добавляем имя файла в метаданные, чтобы нейросеть знала источник
        chunk.metadata["source"] = os.path.basename(file_path)

    # Сохраняем в ChromaDB
    vectordb = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embedding_function
    )
    vectordb.add_documents(chunks)
    
    return len(chunks)

def get_relevant_context(query: str, user_id: int, k: int = 5) -> str:
    """Ищет релевантные куски текста."""
    vectordb = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embedding_function
    )
    
    results = vectordb.similarity_search(
        query, 
        k=k, 
        filter={"user_id": str(user_id)}
    )
    
    # Формируем контекст с указанием источника
    context_parts = []
    for doc in results:
        source_name = doc.metadata.get("source", "Неизвестный файл")
        context_parts.append(f"📄 Источник: {source_name}\n{doc.page_content}")

    return "\n\n---\n\n".join(context_parts)

def clear_user_memory(user_id: int):
    """Очистка памяти (упрощенная)"""
    pass