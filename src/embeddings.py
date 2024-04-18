import logging

from langchain_openai import OpenAIEmbeddings

logger = logging.getLogger(__name__)


class Embeddings:
    def __init__(self):
        logger.debug("Initializing LanguageModel")
        self.embedding_function = OpenAIEmbeddings(
            model="text-embedding-3-large")

    def embed_documents(self, docs):
        logger.debug(f"Generating embedding for doc: {docs}")
        return self.embedding_function.embed_documents(docs)

    def embed_query(self, query):
        logger.debug(f"Generating embedding for query: {query}")
        return self.embedding_function.embed_query(query)
