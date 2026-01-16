# 🧠 AI-Powered Knowledge Agent (Django RAG)

## 📖 Project Overview
This project is an **Agentic RAG (Retrieval-Augmented Generation) Application** migrated from Streamlit to **Django**. It allows users to chat with the content of any website by providing a URL. The system autonomously crawls, extracts, indexes, and retrieves information to answer queries with high contextual accuracy.

The application features a premium dark/vibrant UI, secure session-based authentication, and a high-performance RAG pipeline.

---

## 🏗️ Architecture Explanation
The application follows a robust MVT (Model-View-Template) architecture optimized for RAG operations:

1.  **Frontend (Templates & Static)**:
    *   **Django Templates**: `index.html` (Chat Dashboard), `login.html` (Secure Auth).
    *   **Vanilla CSS/JS**: Custom designed with glassmorphism, micro-animations, and real-time loading indicators for indexing and chatting.

2.  **Django Backend**:
    *   **Views & Routing**: Handles authentication, session management, and API endpoints for indexing and chat.
    *   **Session State**: Tracks chat history and indexing status per user.

3.  **Ingestion Pipeline**:
    *   **Crawler**: Multi-page BFS crawling using `requests` and `BeautifulSoup`.
    *   **Extractor**: Clean content retrieval via `trafilatura`.
    *   **Chunker**: Semantic splitting using LangChain's `RecursiveCharacterTextSplitter`.

4.  **Vector Store & RAG**:
    *   **Embedder**: Local `all-MiniLM-L6-v2` embeddings (cached for sub-second latency).
    *   **Vector DB**: Dual-support for **ChromaDB** (local persistence) and **Pinecone** (cloud production).
    *   **QA Chain**: LangChain `load_qa_chain` using Groq's high-speed inference.

---

## 🛠️ Frameworks & Libraries
*   **Django**: Core web framework for security, routing, and session management.
*   **LangChain**: Orchestrates the RAG pipeline and vector database integrations.
*   **Groq SDK**: Provides ultra-fast LLM inference.
*   **Sentence-Transformers**: Used for local embedding generation.
*   **ChromaDB / Pinecone**: Production-grade vector storage solutions.
*   **BeautifulSoup4 / Trafilatura**: Web scraping and text extraction.

---

## 🤖 LLM Model
**Model**: `llama-3.3-70b-versatile` (via **Groq API**)

**Why this choice?**
*   **Ultra-Low Latency**: Groq's LPU engine provides near-instant tokens-per-second, making the chat feel fluid.
*   **High Intelligence**: Llama 3.3 70B provides reasoning capabilities matching GPT-4 class models, essential for accurate information retrieval.

---

## 🗄️ Vector Database
**Provider**: **ChromaDB** (Default) / **Pinecone** (Optional)

**Why Chroma?**
*   Provides a zero-config, persistent local database that works offline and is perfect for rapid development and private data hosting.

**Why Pinecone?**
*   Used for larger scale deployments where a managed serverless vector store is required for high availability.

---

## 🔢 Embedding Strategy
**Strategy**: Local HuggingFace Embeddings (`all-MiniLM-L6-v2`)
*   **Efficiency**: Running embeddings locally eliminates API costs and reduces network latency during the ingestion phase.
*   **Performance**: 384-dimensional vectors provide a perfect balance between search accuracy and computation speed.
*   **Optimization**: Models are pre-downloaded and cached on the first run for instant subsequent starts.

---

## 🚀 Setup and Run Instructions

### Prerequisites
*   Python 3.11+
*   Groq API Key (and optionally Pinecone API Key)

### 1. Installation
```powershell
git clone https://github.com/Mrigank23012023/Web-chat-Django.git
cd Web-Chat
python -m venv .venv_py311
.venv_py311\Scripts\activate
pip install -r requirements.txt
```

### 2. Configuration
Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_key_here
VECTOR_STORE_PROVIDER=chroma # or pinecone
PINECONE_API_KEY=your_pinecone_key_here # if using pinecone
```

### 3. Database & Auth
```powershell
python manage.py migrate
# Use existing admin / password or create new
python manage.py createsuperuser
```

### 4. Run
```powershell
run_server_django.bat
```
App will be available at: `http://127.0.0.1:8000/`

---

## ⚠️ Assumptions & Limitations

### Assumptions
*   **Content Type**: Assumes the target URL contains indexable HTML text.
*   **Language**: Optimized for English-language websites.

### Limitations
*   **JS-Heavy Sites**: Basic crawler may miss content on sites that require heavy JavaScript execution (e.g., React SPAs).
*   **Storage**: Free-tier ChromaDB is local to the machine; data is not shared between different deployment instances unless using Pinecone.

### Future Improvements
*   **Browser-Based Crawling**: Integrate Playwright/Selenium for indexing dynamic SPAs.
*   **Multi-Agent Mode**: Use LangGraph to implement self-correcting retrieval steps.
*   **Advanced Auth**: Full user registration and OAuth (Google/GitHub) integration.
