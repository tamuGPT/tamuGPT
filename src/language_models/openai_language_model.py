import os
import logging

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from src.language_models.language_model import LanguageModel
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

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

    def generate_prompt(self, context_text, question_text):
        logger.debug(f"Generating prompt with context:"
                     f"{context_text} and question: {question_text}")
        return self.prompt_template.format(context=context_text, question=question_text)

    def generate_summary_prompt(self, context_text, question_text):
        logger.debug(f"Generating summary prompt with content:"
                     f"{context_text} and question: {question_text}")
        return self.prompt_template.format(context=context_text, question=question_text)

    def invoke(self, query, vector_store):
        parser = StrOutputParser()
        chain = (
            {"context": vector_store.as_retriever(), "question": RunnablePassthrough()}
            | self.prompt_template
            | self.model
            | parser
        )

        logger.debug(f"Predicting response with prompt: {query}")
        return chain.invoke(query)
