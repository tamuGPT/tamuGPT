from langchain_openai.chat_models import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from config import AppConfig
from dotenv import load_dotenv, find_dotenv
import pinecone
from langchain_community.vectorstores import Pinecone
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
import os
from langchain_pinecone import PineconeVectorStore
from langchain.chains import RetrievalQA
import html


def load_document(file):
    nombre, extension = os.path.splitext(file) 
    if extension == '.html':
        from langchain_community.document_loaders import UnstructuredHTMLLoader
        print(f'load {file}...')
        loader = UnstructuredHTMLLoader(file)
    elif extension == '.txt':
        from langchain_community.document_loaders import TextLoader  
        print(f'load {file}...')
        loader = TextLoader(file)
    elif extension == '.pdf':
        from langchain_community.document_loaders import PyPDFLoader
        print(f'load {file}...')
        loader = PyPDFLoader(file)
    elif extension == '.docx':
        from langchain_community.document_loaders import Docx2txtLoader
        print(f'load {file}...')
        loader = Docx2txtLoader(file)
    else:
        print('The document format is not supported!')
        return None

    data = loader.load()

    if extension == '.html':
        data = html.unescape(data)

    # print(data)
    
    return data


def split (data, chunk_size=150):
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=20)
    fragments = text_splitter.split_documents(data)
    return fragments

def creating_vectors(index_name):
    
    embeddings = OpenAIEmbeddings()

    vectors = PineconeVectorStore.from_documents(
        fragments, embeddings, index_name=index_name
    )
    print('Ok')
        
    return vectors

def queries(vectors, query):

    llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=1)
    retriever = vectors.as_retriever(search_type='similarity', search_kwargs={'k': 3})
    chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    
    answer = chain.invoke(query)
    return answer

config = AppConfig()

OPENAI_API_KEY = config.OPENAI_API_KEY
PINECONE_API_KEY = config.PINECONE_API_KEY

model = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-3.5-turbo")

# plain_model_res = model.invoke("When is the first day of class for Spring 2024 term at TAMU?")

parser = StrOutputParser()

chain = model | parser

query = "What are the Professor James Caverlee's Recent publications?"

print("QUERY")
print(query)
print("Without RAG")
chain_res = chain.invoke(query)

print("Answer\t", chain_res)

document = "search_results.html"
content = load_document(document)
# print("content\n",content)

fragments = split(content)
# print(len(fragments))

index_name = 'tamu-gpt-index'
vectors = creating_vectors(index_name)


# question = 'When is the graduation ceremony for masters students at TAMU?'
# answer = queries(vectors, question)

# print(vectors.similarity_search("Where is the graduation ceremony at TAMU?")[:3])
# print(answer)
print("-------------------------------------------")




from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain.prompts import ChatPromptTemplate

template = """
Answer the question based on the context below. If you can't 
answer the question, reply "I don't know".

Context: {context}

Question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)


chain = (
    {"context": vectors.as_retriever(), "question": RunnablePassthrough()}
    | prompt
    | model
    | parser
)


######################## WORKS ############################################

print("With RAG")
answer = chain.invoke(query)

print("Answer\t", answer)








