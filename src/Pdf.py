import streamlit as st
import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from html_templates import css, user_template, bot_template
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv

load_dotenv()

groq_api_key = os.getenv('GROQ_API_KEY')
pinecone_api_key = os.getenv('PINECORN_API_KEY')

index_name = "chatwithpdf"
pc = Pinecone(api_key=pinecone_api_key)

if index_name not in pc.list_indexes().names():
    try:
        pc.create_index(
            name=index_name,
            dimension=384,  # Ensure this matches your embedding dimension
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )
    except Exception as e:
        st.error(f"Error creating Pinecone index: {e}")
        st.stop()

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vectorstore(text_chunks):
    if not text_chunks:
        raise ValueError("No text chunks to process for embeddings.")
    
    embeddings = HuggingFaceBgeEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",  
        model_kwargs={'device':'cpu'},
        encode_kwargs={'normalize_embeddings':True}
    )
    
    vectorstore = PineconeVectorStore.from_texts(
        text_chunks,
        index_name=index_name,
        embedding=embeddings
    )
    
    return vectorstore

def get_conversation_chain(vectorstore):
    llm = ChatGroq(groq_api_key=groq_api_key, model_name="Llama3-8b-8192", max_tokens=8192)
    
    prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

    Context: {context}
    Question: {input}

    Answer:""")
    
    document_chain = create_stuff_documents_chain(llm, prompt)
    
    retriever = vectorstore.as_retriever()
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    
    return retrieval_chain

def handle_user_input(user_question):
    if st.session_state.conversation is None:
        st.error("Conversation is not initialized. Please upload and process the PDFs first.")
        return
    
    response = st.session_state.conversation.invoke({"input": user_question})
    st.session_state.chat_history.append(("Human", user_question))
    st.session_state.chat_history.append(("AI", response['answer']))
    
    for role, message in st.session_state.chat_history:
        if role == "Human":
            st.write(user_template.replace("{{MSG}}", message), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}", message), unsafe_allow_html=True)

def show_chat_page():
    st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":books:")
    st.write(css, unsafe_allow_html=True)
    
    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    
    if "chat_history" not in st.session_state or st.session_state.chat_history is None:
        st.session_state.chat_history = []
    
    st.header("Chat with multiple PDFs :books:")
    
    if st.button("Go to Home Page"):
        st.session_state.current_page = "Home"
        st.rerun()

    user_question = st.text_input("Ask a question about your documents:") 
    if user_question:
        handle_user_input(user_question)
    
    with st.sidebar:
        st.sidebar.title("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs", type=["pdf"], accept_multiple_files=True)
        if st.button("Process"):
            if pdf_docs:
                with st.spinner("Processing..."):
                    raw_text = get_pdf_text(pdf_docs)
                    if not raw_text:
                        st.error("No text could be extracted from the uploaded PDFs.")
                        return
                    
                    text_chunks = get_text_chunks(raw_text)
                    if not text_chunks:
                        st.error("No text chunks could be created from the extracted text.")
                        return
                    
                    vectorstore = get_vectorstore(text_chunks)
                    st.success("Vector store created successfully!")
                    
                    st.session_state.conversation = get_conversation_chain(vectorstore)
            else:
                st.error("Please upload at least one PDF file.")

if __name__ == '__main__':
    show_chat_page()
