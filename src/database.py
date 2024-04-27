import logging

from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings

logger = logging.getLogger(__name__)


class Database:
    def __init__(self, api_key):
        self.pc = Pinecone(api_key=api_key)
        self.index = self.pc.Index('langchainvector')
        logger.debug(f"Initializing database")

    def search(self, query_text, k=3):
        embeddings = OpenAIEmbeddings()
        vectors = embeddings.embed_query(query_text)
        results = self.index.query(vector=vectors,top_k=k,include_metadata=True)
        logger.debug(f"Searching database for query: {query_text}")
        query_results = []
        for result in results['matches']:
            qresult = {
                'url': result['metadata']['source'],
                'metadata': {'content': result['metadata']['text']}
            }

            query_results.append(qresult)
        return query_results
