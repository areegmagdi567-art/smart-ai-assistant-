import os
from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import REGULATIONS_DIR, OPENAI_API_KEY

# ضبط مفتاح الـ API إذا لم يكن مخزناً في النظام
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY


def initialize_knowledge_base():
  # 1. تحميل ملفات الـ PDF من مجلد regulations
  loader = PyPDFDirectoryLoader(REGULATIONS_DIR)
  documents = loader.load()

  # 2. تقطيع النصوص إلى أجزاء صغيرة (Chunks)
  text_splitter = RecursiveCharacterTextSplitter(
      chunk_size=1000, chunk_overlap=200
  )
  docs = text_splitter.split_documents(documents)

  # 3. تحويل النصوص إلى Vector Embeddings وتخزينها محلياً
  embeddings = OpenAIEmbeddings()
  vectorstore = Chroma.from_documents(docs, embeddings)

  return vectorstore.as_retriever(
      search_kwargs={"k": 3}
  )


def get_conversation_chain():
  retriever = initialize_knowledge_base()

  # استخدام نموذج OpenAI للردود
  llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.2)

  # بناء سلسلة محادثات تدعم استرجاع السياق (RAG)
  from langchain.memory import ConversationBufferMemory

  memory = ConversationBufferMemory(
      memory_key="chat_history", return_messages=True
  )

  conversation_chain = ConversationalRetrievalChain.from_llm(
      llm=llm, retriever=retriever, memory=memory
  )

  return conversation_chain
