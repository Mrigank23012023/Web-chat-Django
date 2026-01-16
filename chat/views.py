import json
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.cache import never_cache
from .config import Config

# Backend imports
from .backend.crawler import Crawler
from .backend.extractor import Extractor
from .backend.cleaner import Cleaner
from .backend.chunker import Chunker
from .backend.vectorstore import VectorStore
from .backend.qa_chain import QAChain
from .backend.embedder import Embedder

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'chat/login.html', {'error': 'Invalid credentials'})
    return render(request, 'chat/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
@ensure_csrf_cookie
@never_cache
def index(request):
    if 'messages' not in request.session:
        request.session['messages'] = []
    return render(request, 'chat/index.html')

@login_required
def clear_chat(request):
    request.session['messages'] = []
    return redirect('index')

# API Endpoints

@login_required
def api_index(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            url_to_index = data.get('url')
            
            if not url_to_index:
                return JsonResponse({'success': False, 'error': 'No URL provided'})

            # Implement Indexing Logic
            crawler = Crawler()
            crawled_pages = crawler.crawl(url_to_index)
            
            extractor = Extractor()
            extracted_data = []
            for page in crawled_pages:
                result = extractor.extract(page['html'])
                if result:
                    extracted_data.append({
                        "url": page['url'], 
                        "text": result['text'], 
                        "title": result['title']
                    })
            
            cleaner = Cleaner()
            chunker = Chunker()
            all_chunks = []
            
            for data in extracted_data:
                clean_text = cleaner.clean(data['text'])
                chunks = chunker.chunk(clean_text, data['url'], data['title'])
                all_chunks.extend(chunks)
            
            embedder = Embedder()
            embedding_function = embedder.get_embedding_function()
            
            vs_wrapper = VectorStore(collection_name="website_content") # Simplified for single user/session demo
            vectorstore = vs_wrapper.create_collection(all_chunks, embedding_function)
            
            # Persist vectorstore info in session if needed, 
            # but since VectorStore is persistent (Chroma/Pinecone), we just need to know it's ready.
            request.session['indexed_url'] = url_to_index
            
            return JsonResponse({'success': True, 'chunks_count': len(all_chunks)})
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
            
    return JsonResponse({'success': False, 'error': 'Invalid method'})

@login_required
def api_chat(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message')
            
            # Save user message
            messages = request.session.get('messages', [])
            messages.append({"role": "user", "content": user_message})
            request.session['messages'] = messages
            
            # RAG Logic
            try:
                embedder = Embedder()
                embedding_function = embedder.get_embedding_function()
                vs_wrapper = VectorStore(collection_name="website_content")
                
                # We need to get the existing vectorstore. 
                # VectorStore wrapper creates/resets in create_collection.
                # We need a way to LOAD it.
                # In Streamlit, it was passed around.
                # Here, we instantiate it again. 
                # Ideally, we should check if it exists.
                # For Chroma, VectorStore(collection_name).as_retriever(...) should work if persisted.
                
                # Temporary fix: Assume it exists if we are chatting.
                # But VectorStore class initialization logic in original code assumes creation?
                # Let's check VectorStore code again.
                # It initializes client.
                # But it doesn't have a "load" method explicit.
                # But as_retriever takes a 'vectorstore' object returned by create_collection.
                # We need to get that object WITHOUT creating it again.
                
                # For Chroma:
                if Config.VECTOR_STORE_PROVIDER == "chroma":
                    from langchain_community.vectorstores import Chroma
                    vectorstore = Chroma(
                        persist_directory=Config.CHROMA_DB_PATH,
                        embedding_function=embedding_function,
                        collection_name="website_content"
                    )
                # For Pinecone:
                elif Config.VECTOR_STORE_PROVIDER == "pinecone":
                    from langchain_pinecone import PineconeVectorStore
                    if Config.PINECONE_API_KEY:
                        import os
                        os.environ["PINECONE_API_KEY"] = Config.PINECONE_API_KEY
                        
                    vectorstore = PineconeVectorStore.from_existing_index(
                        index_name=Config.PINECONE_INDEX_NAME,
                        embedding=embedding_function
                    )
                
                retriever = vs_wrapper.as_retriever(vectorstore)
                qa_chain = QAChain(retriever)
                
                # Chat History for Context
                history_window = messages[-5:]
                chat_history_str = ""
                for msg in history_window:
                    role_label = "Human" if msg["role"] == "user" else "AI"
                    chat_history_str += f"{role_label}: {msg['content']}\n"
                
                result = qa_chain.answer(user_message, chat_history=chat_history_str)
                
                answer_text = result['answer']
                sources = [{"source": doc.metadata.get('source'), "title": doc.metadata.get('title')} for doc in result['sources']]
                
                # Save assistant message
                # Formatting sources in HTML is done in JS for display, but here we save raw text?
                # Or we can save HTML. Let's save plain text for now.
                messages.append({"role": "assistant", "content": answer_text})
                request.session['messages'] = messages
                request.session.modified = True
                
                return JsonResponse({'answer': answer_text, 'sources': sources})

            except Exception as e:
                return JsonResponse({'answer': f"Error: {str(e)}"})
                
        except Exception as e:
            return JsonResponse({'error': str(e)})

    return JsonResponse({'error': 'Invalid method'})
