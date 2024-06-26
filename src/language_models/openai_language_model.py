import json
import os
import logging

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from src.language_models.language_model import LanguageModel

logger = logging.getLogger(__name__)


class OpenAILanguageModel(LanguageModel):
    def __init__(self,
                 template_path=os.path.join(os.path.dirname(__file__), "../templates", "chat_template.txt")):
        logger.debug("Initializing OpenAI Language Model")
        self.model = ChatOpenAI()

        self.template_path = template_path
        self.template = self._load_template(self.template_path)
        self.prompt_template = ChatPromptTemplate.from_template(self.template)

    @staticmethod
    def _load_template(template_path):
        try:
            logger.debug(f"Loading template from path: {template_path}")
            with open(template_path, "r") as file:
                return file.read()
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Template file '{template_path}' not found.")

    def generate_prompt(self, **kwargs):
        logger.debug(f"Generating prompt with kwargs: {json.dumps(kwargs, indent=4)}")
        return self.prompt_template.format(**kwargs)

    def invoke(self, prompt):
        logger.debug(f"Predicting response with prompt: {prompt}")
        return self.model.invoke(prompt)
