import gradio as gr

import os

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_community import embeddings
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import RetrievalQA
from langchain.memory import ConversationSummaryMemory
from langchain.prompts import PromptTemplate
from langchain.llms import Ollama
from langchain.text_splitter import CharacterTextSplitter

def llm_response(uploadedFile, prompt):
    model_local = ChatOllama(model="ollama2")
    print(uploadedFile)
    print(prompt)
    # data_path = "./data/Elden_Ring.pdf"
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=2000,
    chunk_overlap=30,
    length_function=len,)

    # doc_splits = text_splitter.split_documents(uploadedFile)
    documents = PyPDFLoader(uploadedFile).load_and_split(text_splitter=text_splitter)

    vectorstore = Chroma.from_documents(
        documents=documents,
        collection_name="rag-chroma",
        embedding=embeddings.ollama.OllamaEmbeddings(model='nomic-embed-text'),
    )
    retriever = vectorstore.as_retriever()

    rag_template =  """Answer the question based only on the following context:
    {context}
    Question: {question}
    """

    rag_prompt = ChatPromptTemplate.from_template(rag_template)

    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | rag_prompt
        | model_local
        | StrOutputParser()
        )
    
    
    # return rag_chain.invoke(prompt)
    return "Hello"
    

inputs = [
    gr.File(label="Upload a text file"),
    gr.Textbox(lines=5, label="Enter prompt text"),
]

uploadedFile = inputs[0]
prompt = inputs[1]

interface=gr.Interface(
    title = "DocAI",
    fn=llm_response,
    inputs=inputs,
    outputs="text"
)
interface.launch()