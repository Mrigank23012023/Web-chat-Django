# 🧠 AI-Powered Website Chatbot (RAG Agent)

## 📖 Project Overview
This project is an **Agentic RAG (Retrieval-Augmented Generation) Application** that allows users to chat with any website. It autonomously crawls, extracts, indexes, and retrieves information from a target URL to answer user queries with high accuracy. 

The application is built with a focus on **modularity, speed, and deployment stability**, supporting both local and cloud environments (Streamlit Cloud).

## 🏗️ Architecture Explanation
The system follows a modular pipeline architecture:

1.  **User Interface (Frontend)**: Built with **Streamlit**, providing a clean, responsive chat interface with sidebar controls and authentication.
2.  **Ingestion Pipeline**:
    *   **Crawler**: Uses `requests` and `BeautifulSoup` to crawl pages (BFS strategy).
    *   **Extractor**: Uses `trafilatura` to extract clean main text from HTML, discarding boilerplate.
    *   **Chunker**: Splits text into semantic chunks using `RecursiveCharacterTextSplitter` with overlap to preserve context.
3.  **Vector Storage & Embedding**:
    *   **Embedder**: Generates 384-dimensional vectors using `sentence-transformers/all-MiniLM-L6-v2`.
    *   **Vector Database**: Supports a **Hybrid Architecture** (configurable via environment variables):
        *   **Pinecone**: For production and cloud deployment (persistent, scalable).
        *   **ChromaDB**: For local development (requires SQLite).
4.  **Retrieval & Generation**:
    *   **Retriever**: Fetches the top-k most relevant chunks based on semantic similarity.
    *   **LLM Chain**: Uses **LangChain** to construct a prompt with context and history, sending it to the **Groq API**.

## 🛠️ Frameworks & Libraries
*   **LangChain**: The backbone for the RAG pipeline, chain orchestration, and vector store abstractions.
*   **Streamlit**: For the interactive web application and session state management.
*   **BeautifulSoup4 / Trafilatura**: For robust web scraping and content extraction.
*   **Sentence-Transformers**: For generating high-quality text embeddings locally.
*   **PySQLite3-Binary**: To ensure database compatibility on modern cloud environments (Streamlit Cloud/Linux).

## 🤖 LLM Model Used
**Model**: `llama-3.3-70b-versatile` (via **Groq**)

**Why this choice?**
*   **Speed**: Groq's LPU inference engine provides near-instant responses, which is critical for a smooth chat experience.
*   **Performance**: The Llama 3.3 70B model offers state-of-the-art reasoning capabilities comparable to GPT-4, ensuring accurate and nuanced answers from the retrieve context.
*   **Cost**: Efficient and often cost-effective for high-throughput applications.

## 🗄️ Vector Database Strategy
**Primary**: **Pinecone** (Serverless)

**Why?**
*   **Cloud Native**: Essential for deployment on ephemeral environments like Streamlit Cloud where local files are lost on restart.
*   **Performance**: Extremely fast vector search at scale.

**Secondary**: **ChromaDB** (Local)
*   Used for local testing to avoid API latency during development.
* 

## 🔢 Embedding Strategy
**Model**: `sentence-transformers/all-MiniLM-L6-v2`
*   **Dimensions**: 384
*   We use a local embedding model (HuggingFace) rather than an API-based one. This reduces latency and cost for the ingestion phase, as we don't need to pay per token for embedding thousands of document chunks.

## 🚀 Setup and Run Instructions

### Prerequisites
*   Python 3.10+
*   Git

### 1. Clone the Repository
```bash
git clone https://github.com/Mrigank23012023/Web-Chat.git
cd Web-Chat
```

### 2. Install Dependencies
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment
Create a `.env` file or set specific Secrets in Streamlit Cloud:

```ini
GROQ_API_KEY=gsk_...
PINECONE_API_KEY=pc_...
VECTOR_STORE_PROVIDER=pinecone   # Options: pinecone, chroma
```

*Note: For Pinecone, create an index named `website-content` with dimensions **384** and metric **cosine**.*

### 4. Run the Application
```bash
streamlit run app.py
```

## ⚠️ Assumptions, Limitations, and Future Improvements

### Assumptions
*   The target website allows crawling (robots.txt is respected but basic headers are used).
*   The content is primarily English text.

### Limitations
*   **Dynamic Content**: Websites heavily reliant on JavaScript (SPA) might not be fully indexed strictly by the `requests` crawler.
*   **Crawling Depth**: Limited to 5 pages by default to prevent timeouts (configurable in `config.py`).
*   **Session Persistence**: Chat history is stored in RAM (session state) and is lost on refresh.

### Future Improvements
*   **Headless Browser**: Integrate `Selenium` or `Playwright` for crawling dynamic JS-heavy sites.
*   **Multi-User DB**: Upgrade to storing chat history in a persistent database (PostgreSQL/Firebase).
*   **File Uploads**: Add support for PDF/Docx indexing alongside URLs.
