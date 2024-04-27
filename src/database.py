import logging

from langchain_pinecone import PineconeVectorStore
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
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
import html

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, index_name):
        logger.debug(f"Initializing database with index name: {index_name}")
        self.index_name = index_name

    def _split_data (self, data, chunk_size=5000):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=0)
        fragments = text_splitter.split_text(data)
        return fragments

    def create_vector_store(self, data):
        fragments = self._split_data(data)
        embeddings = OpenAIEmbeddings()

        vector_store = PineconeVectorStore.from_texts(
            fragments, embeddings, index_name = self.index_name
        )
            
        return vector_store

    def search(self, query_text, k=3):
        logger.debug(f"Searching database for query: {query_text}")
        return self.db.similarity_search_with_relevance_scores(query_text, k=k)
