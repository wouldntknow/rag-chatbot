# Document Q&A Agent

A Retrieval-Augmented Generation (RAG) chatbot that lets you upload PDF, DOCX, or TXT documents and ask questions about them in natural language. Built with an agentic architecture (OpenAI Agents SDK running on Gemini), ChromaDB for vector storage, and a Chainlit chat interface.

## How it works

1. You upload one or more documents (PDF, DOCX, or TXT) through the chat.
2. Each document is split into overlapping text chunks and converted into vector embeddings using Gemini's embedding model.
3. The embeddings are stored in a local ChromaDB vector store.
4. When you ask a question, the agent retrieves only the chunks most relevant to that question (not the whole document) and uses them, along with Gemini's language model, to generate an answer grounded in your documents.
5. If the answer isn't in your documents, the agent says so clearly instead of guessing.

This is a proper RAG pipeline rather than a simple "attach file to the model's context" approach — it scales to large documents and only pulls in what's relevant to each specific question.

## Features

- 📎 Upload PDF, DOCX, or TXT files at any point in the conversation (button never disappears, more documents can be added anytime)
- 🔍 Semantic search over your documents using vector embeddings, not keyword matching
- 🤖 Agentic design using the OpenAI Agents SDK, running on Google Gemini via its OpenAI-compatible endpoint
- 🧠 Answers are grounded only in retrieved document content — the agent is instructed not to invent information
- 💬 Simple Chainlit chat UI

## Tech stack

| Component            | Technology                                   |
|-----------------------|-----------------------------------------------|
| Chat interface         | [Chainlit](https://docs.chainlit.io/)         |
| Agent framework        | [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) (`openai-agents`) |
| LLM                    | Google Gemini (`gemini-2.5-flash`), via Gemini's OpenAI-compatible API |
| Embeddings              | Google Gemini (`gemini-embedding-001`)       |
| Vector store            | [ChromaDB](https://www.trychroma.com/) (local, persisted to disk) |
| Document loading         | `langchain_pdfmuse` (PDF), `Docx2txtLoader` (DOCX), `TextLoader` (TXT) |
| Text splitting           | `langchain_text_splitters` (`RecursiveCharacterTextSplitter`) |

## Project structure

```
your-repo/
├── main.py                 # Chainlit entrypoint: UI, upload handling, message loop
├── .env                     # API keys (not committed)
├── .chainlit/
│   └── config.toml          # Chainlit configuration
└── src/
    ├── __init__.py
    ├── config.py             # Environment variables and constants
    ├── embeddings.py          # Gemini embeddings wrapper (LangChain Embeddings interface)
    ├── ingestion.py            # Document loading + chunking (PDF/DOCX/TXT)
    ├── vectorstore.py           # ChromaDB setup and document storage
    ├── retriever.py              # Similarity search over the vector store
    └── agent.py                   # Agent definition, tools, and Gemini wiring
```

## Prerequisites

- Python 3.10+
- A [Google Gemini API key](https://aistudio.google.com/apikey)

## Installation

1. **Clone the repo and enter the project directory.**

2. **Create and activate a virtual environment.**

   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies.**

   ```bash
   pip install chainlit langchain langchain-core langchain-chroma langchain-text-splitters langchain-community langchain-pdfmuse google-genai python-dotenv openai openai-agents docx2txt
   ```

4. **Set up environment variables.**

   Create a `.env` file in the project root:

   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

## Running the app

```bash
chainlit run main.py -w
```

- `-w` enables auto-reload on file changes (optional, useful during development).
- The app opens automatically at `http://localhost:8000`.

## Usage

1. On first load, you'll be prompted to upload a document (PDF, DOCX, or TXT).
2. Once processed, ask any question about it in the chat.
3. Use the **📎 Upload a document** button, visible under every message, to add more documents to the same session at any time.
4. If a question can't be answered from the uploaded documents, the agent will tell you directly rather than making something up.

## Known limitations

- **Shared vector collection:** All uploaded documents in a running instance are stored in the same ChromaDB collection (`pdf_documents`). Retrieval is not scoped per-session or per-user, so documents from different uploads can be retrieved together. To reset the store, delete the `chroma_db/` directory.
- **No conversation memory:** Each question is handled independently; the agent does not currently retain context from earlier turns in the conversation.
- **Local-only vector store:** ChromaDB runs in embedded/local mode and persists to disk — it is not a hosted/multi-instance deployment.

## License

All rights reserved. This code is shared for portfolio/demonstration purposes only. No permission is granted to copy, modify, distribute, or use this code without explicit written consent from the author.