import os
from dotenv import load_dotenv


class AppConfig:
    def __init__(self):
        load_dotenv()

        self.BASE_PATH = os.path.dirname(__file__)
        self.DATA_PATH = os.path.join(self.BASE_PATH, "data")
        self.CRAWLED_DATA_PATH = os.path.join(self.DATA_PATH, "crawled")
        self.DOCUMENTS_PATH = os.path.join(self.DATA_PATH, "documents")
        self.DATABASE_PATH = os.path.join(self.DATA_PATH, "database")

        self.TEMPLATE_PATH = os.path.join(
            self.BASE_PATH, "src", "templates", "chat_template.txt")

        # throw error if not found
        self.OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
        self.GOOGLE_SEARCH_API_KEY = os.environ["GOOGLE_SEARCH_API_KEY"]
        self.GOOGLE_CSE_ID = os.environ["GOOGLE_CSE_ID"]
        self.GOOGLE_CSE_API_KEY = os.environ["GOOGLE_CSE_API_KEY"]
        self.PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]