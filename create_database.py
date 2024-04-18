import logging
import os
import shutil

from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.chroma import Chroma

from config import AppConfig
from src.embeddings import Embeddings

logger = logging.getLogger(__name__)


class DatabaseGenerator:
    def __init__(self, data_path, chroma_path):
        self.data_path = data_path
        self.db_path = chroma_path
        self.embeddings = Embeddings()

    def generate_database(self):
        documents = self.load_documents()
        chunks = self.split_text(documents)
        self.save_to_chroma(chunks)

    def load_documents(self):
        loader = DirectoryLoader(self.data_path, glob="*.html")
        documents = loader.load()
        return documents

    @staticmethod
    def split_text(documents):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=300,
            chunk_overlap=100,
            length_function=len,
            add_start_index=True,
        )
        chunks = text_splitter.split_documents(documents)
        return chunks

    def save_to_chroma(self, chunks):
        if os.path.exists(self.db_path):
            shutil.rmtree(self.db_path)

        db = Chroma.from_documents(
            chunks,
            self.embeddings.embedding_function,
            persist_directory=self.db_path
        )
        db.persist()
        logger.info(f"Saved {len(chunks)} chunks to {self.db_path}.")


if __name__ == "__main__":
    config = AppConfig()

    logger.info(f"Generating database from {
                config.DATA_PATH} to {config.DATABASE_PATH}.")
    generator = DatabaseGenerator(config.DATA_PATH, config.DATABASE_PATH)
    generator.generate_database()
    logger.info("Database generation complete.")
