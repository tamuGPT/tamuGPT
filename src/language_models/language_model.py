import logging

from src.language_models.openai_language_model import OpenAILanguageModel

logger = logging.getLogger(__name__)


class LanguageModel(OpenAILanguageModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logger.debug("Initializing LanguageModel")
