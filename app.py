import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings,HuggingFaceInstructEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css,bot_template,user_template
from langchain.llms import HuggingFaceHub


def get_pdf_text(pdf_docs):
    text=""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="/n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )

    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    # embeddings = OpenAIEmbeddings()
    embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
    vectorstore = FAISS.from_texts(texts=text_chunks,embedding=embeddings)
    return vectorstore

def get_conversation_chain(vectorstore):
    # llm = ChatOpenAI()
    llm = HuggingFaceHub(repo_id="openai-community/openai-gpt", model_kwargs={"temperature":0.5, "max_length":1024})
    memory = ConversationBufferMemory(memory_key="chat_history",return_messages=True)
    converstation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,    
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return converstation_chain

def handle_user_input(user_input):
    response = st.session_state.conversation({'question': user_input})

    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)

def main():
    load_dotenv()
    st.set_page_config(page_title="kurma",page_icon=":fox:")
    st.write(css,unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None  #remains the same for the session

    st.header("Chat with multiple PDF's")

    user_input = st.text_input("Enter your message here")
    if user_input:
        handle_user_input(user_input)



    # st.write(user_template.replace("{{MSG}}","Hello bot"),unsafe_allow_html=True)
    # st.write(bot_template.replace("{{MSG}}","Hello human"),unsafe_allow_html=True)

    with st.sidebar:
        st.subheader("Your Docs")
        pdf_docs = st.file_uploader("Upload your PDF",accept_multiple_files=True)
        
        if st.button("Process"):
            with st.spinner("Processing..."):
                
            #get pdf text
                raw_text = get_pdf_text(pdf_docs)

            #get the text chunks
                text_chunks = get_text_chunks(raw_text)
                # st.write(text_chunks)

            #create vector store
                vector_store = get_vector_store(text_chunks)
                # st.write(vector_store)

            #converstion chain
                st.session_state.conversation = get_conversation_chain(vector_store)


if __name__ == "__main__":
    main()