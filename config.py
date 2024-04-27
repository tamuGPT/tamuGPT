import logging
import logging.config
import os
from dotenv import load_dotenv


class AppConfig:
    def __init__(self, log_level="INFO"):
        load_dotenv()

        self.BASE_PATH = os.path.dirname(__file__)
        self.DATA_PATH = os.path.join(self.BASE_PATH, "data")
        self.CRAWLED_DATA_PATH = os.path.join(self.DATA_PATH, "crawled")
        self.DOCUMENTS_PATH = os.path.join(self.DATA_PATH, "documents")
        self.DATABASE_PATH = os.path.join(self.DATA_PATH, "database")
        self.PINECONE_API_KEY = os.environ['PINECONE_API_KEY']
        self.TEMPLATE_PATH = os.path.join(
            self.BASE_PATH, "src", "templates", "chat_template.txt")
        self.SUMMARY_TEMPLATE_PATH = os.path.join(
            self.BASE_PATH, "src", "templates", "summary_template.txt")
        self.RANK_TEMPLATE_PATH = os.path.join(
            self.BASE_PATH, "src", "templates", "rank_template.txt")

        # throw error if not found
        self.OPENAPI_API_KEY = os.environ["OPENAI_API_KEY"]
        self.GOOGLE_SEARCH_API_KEY = os.environ["GOOGLE_SEARCH_API_KEY"]
        self.GOOGLE_CSE_ID = os.environ["GOOGLE_CSE_ID"]
        self.GOOGLE_CSE_API_KEY = os.environ["GOOGLE_CSE_API_KEY"]

        self.logging_config = self.get_logger(log_level)

    def get_logger(self, level="INFO"):
        logging_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "standard": {
                    "format": "[%(asctime)s] [%(levelname)s] [%(name)s] [%(funcName)s:%(lineno)d] %(message)s"
                }
            },
            "handlers": {
                "console": {
                    "level": level,
                    "class": "logging.StreamHandler",
                    "formatter": "standard"
                },
                "debug-logfile": {
                    "level": "DEBUG",
                    "class": "logging.FileHandler",
                    "filename": os.path.join(self.BASE_PATH, "logs", "debug.log"),
                    "formatter": "standard"
                },
                "info-logfile": {
                    "level": "INFO",
                    "class": "logging.FileHandler",
                    "filename": os.path.join(self.BASE_PATH, "logs", "info.log"),
                    "formatter": "standard"
                },
                "error-logfile": {
                    "level": "ERROR",
                    "class": "logging.FileHandler",
                    "filename": os.path.join(self.BASE_PATH, "logs", "error.log"),
                    "formatter": "standard"
                },
            },
            "loggers": {
                "__main__": {
                    "level": level,
                    "handlers": ["console", "debug-logfile", "info-logfile", "error-logfile"],
                    "propagate": True,
                },
                "src": {
                    "level": level,
                    "handlers": ["console", "debug-logfile", "info-logfile", "error-logfile"],
                    "propagate": True,
                },
            }
        }
        return logging_config
