import logging

from langchain.vectorstores.chroma import Chroma

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, db_path):
        logger.debug(f"Initializing database with path: {db_path}")
        self.db = Chroma(persist_directory=db_path)

    def search(self, query_text, k=3):
        logger.debug(f"Searching database for query: {query_text}")
        return self.db.similarity_search_with_relevance_scores(query_text, k=k)
