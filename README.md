📄 Business Doc Assistant Bot

A powerful Telegram bot designed to analyze corporate documents (PDF, DOCX, TXT, and more) and answer questions based strictly on their content. The bot utilizes RAG (Retrieval-Augmented Generation) to ensure accuracy and prevent AI hallucinations by grounding responses in your specific data.
✨ Key Features

    Multi-format Support: Process PDF, DOCX, CSV, TXT, HTML, and more.

    Intelligent Search: Uses ChromaDB (Vector Database) to find the most relevant parts of your documents instantly.

    Privacy-First: Context is filtered by user_id, ensuring that your documents are only accessible to you.

    Strict AI Persona: Powered by DeepSeek (via OpenRouter), the bot follows a professional business style and refuses to invent information not found in the documents.

    Source Citations: Every answer includes the name of the source file for verification.

🛠 Tech Stack

    Bot Framework: aiogram 3.x

    LLM Orchestration: LangChain

    Vector Database: ChromaDB

    Embeddings: sentence-transformers/all-MiniLM-L6-v2 (HuggingFace)

    AI Model: DeepSeek-R1 via OpenRouter

🚀 Quick Start
1. Clone the repository
code Bash

git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

2. Install Dependencies

It is recommended to use a virtual environment:
code Bash

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

Note: Ensure you have pypdf, docx2txt, langchain-chroma, and aiogram installed.
3. Configuration

Create a .env file in the root directory and fill in your credentials:
code Env

BOT_TOKEN=your_telegram_bot_token
OPENROUTER_API_KEY=your_openrouter_api_key
MODEL_NAME=deepseek/deepseek-r1:free

4. Run the Bot
code Bash

python main.py

📂 Project Structure

    main.py — Entry point. Initializes the bot and dispatcher.

    handlers/user_mode.py — Main logic for file uploads and Q&A sessions.

    services/vector_store.py — Logic for document loading, text splitting (RecursiveCharacterTextSplitter), and ChromaDB integration.

    services/llm_client.py — Handles communication with the LLM via OpenRouter.

    keyboards/builders.py — Custom Reply/Inline keyboards.

    states/user_states.py — FSM (Finite State Machine) definitions.

📝 How to Use

    Upload Documents: Click "📂 Загрузить документы" and send your files (e.g., a PDF contract or a TXT manual).

    Indexing: The bot splits the text into chunks and saves them into the local vector store. Click "✅ Завершить загрузку" when finished.

    Ask Questions: Click "💬 Задать вопрос" and ask anything related to your files.

    Get Answers: The bot will retrieve the relevant context and provide a concise, professional answer based only on your documents.

⚠️ Important Notes

    Local Storage: The vector database is stored locally in the ./chroma_db folder.

    Context Window: The bot currently retrieves the top 5 most relevant text chunks to generate an answer.

    Hallucination Protection: The system prompt is configured to make the bot say "I don't know" if the information is missing from the documents.
