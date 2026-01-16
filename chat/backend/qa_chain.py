class QAChain:
    
    def __init__(self, vectorstore_retriever):
        import logging
        from langchain_groq import ChatGroq
        from langchain.chains.question_answering import load_qa_chain
        from langchain.prompts import PromptTemplate
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

{context}

Current Conversation:
{chat_history}

Question: {question}
Answer:"""
        
        self.prompt = PromptTemplate(
            template=template, 
            input_variables=["context", "chat_history", "question"]
        )
        
        self.chain = load_qa_chain(
            llm=self.llm, 
            chain_type="stuff", 
            prompt=self.prompt
        )
    
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
            
            inputs = {"input_documents": docs, "question": query, "chat_history": chat_history}
            
            if hasattr(self.chain, 'invoke'):
                response = self.chain.invoke(inputs, return_only_outputs=True)
                answer_text = response['output_text']
            else:
                response = self.chain(inputs, return_only_outputs=True)
                answer_text = response['output_text']
            
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
