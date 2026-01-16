class QAChain:
    
    def __init__(self, vectorstore_retriever):
        import logging
        from langchain_groq import ChatGroq
        from langchain_core.prompts import PromptTemplate
        from langchain_core.output_parsers import StrOutputParser
        from langchain_core.runnables import RunnablePassthrough
        from chat.config import Config
        
        self.logger = logging.getLogger(__name__)
        self.retriever = vectorstore_retriever
        
        self.llm = ChatGroq(
            model_name=Config.LLM_MODEL_NAME,
            temperature=Config.LLM_TEMPERATURE,
            groq_api_key=Config.GROQ_API_KEY
        )
        
        template = """Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say 'The answer is not available on the provided website.', don't try to make up an answer.

Context:
{context}

Current Conversation:
{chat_history}

Question: {question}
Answer:"""
        
        self.prompt = PromptTemplate(
            template=template, 
            input_variables=["context", "chat_history", "question"]
        )
        
        # Build chain using LCEL
        self.chain = self.prompt | self.llm | StrOutputParser()
    
    def answer(self, query: str, chat_history: str = ""):
        self.logger.info(f"Generating answer for query: {query}")
        try:
            if hasattr(self.retriever, 'invoke'):
                docs = self.retriever.invoke(query)
            else:
                docs = self.retriever.get_relevant_documents(query)
            
            if not docs:
                self.logger.warning(f"No relevant documents found for: {query}")
                return {
                    "answer": "The answer is not available on the provided website.",
                    "sources": []
                }
            
            # Format context from documents
            context = "\n\n".join([doc.page_content for doc in docs])
            
            # Invoke chain with formatted inputs
            answer_text = self.chain.invoke({
                "context": context,
                "chat_history": chat_history,
                "question": query
            })
            
            return {
                "answer": answer_text,
                "sources": docs
            }
            
        except Exception as e:
            self.logger.error(f"Error executing QA chain: {e}", exc_info=True)
            return {
                "answer": f"An error occurred: {str(e)}",
                "sources": []
            }
