
try:
    import langchain
    print(f"LangChain Version: {langchain.__version__}")
    from langchain_community.chains.question_answering import load_qa_chain
    from langchain_core.prompts import PromptTemplate
    print("✅ load_qa_chain and PromptTemplate imported successfully")
except Exception as e:
    print(f"❌ Import Failed: {e}")
