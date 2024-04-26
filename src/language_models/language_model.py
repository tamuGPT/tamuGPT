import logging

logger = logging.getLogger(__name__)


class LanguageModel:
    def generate_prompt(self, context_text, question_text):
        raise NotImplementedError(
            "generate_prompt method must be implemented by subclasses")

    def invoke(self, prompt):
        raise NotImplementedError(
            "invoke method must be implemented by subclasses")
