import os
import argparse
import logging
import logging.config

from config import AppConfig
from src.database import Database
from src.language_models.openai_language_model import OpenAILanguageModel

logger = logging.getLogger(__name__)


def main():
    config = AppConfig(log_level="DEBUG")
    logging.config.dictConfig(config.logging_config)

    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    # db = Database(config.DATABASE_PATH)

    # results = db.search(query_text)
    # if len(results) == 0 or results[0][1] < 0.7:
    #     logger.info(f"Unable to find matching results.")
    #     return

    # extract context text
    # context_text = "\n\n---\n\n".join(
    #     [doc.page_content for doc, _score in results])

    context_text = "This is Bharath"
    logger.info(f"Context: {context_text}")

    model = OpenAILanguageModel(config.TEMPLATE_PATH)
    prompt = model.generate_prompt(context_text, query_text)
    response_text = model.invoke(prompt)

    # get sources
    # sources = [doc.metadata.get("source", None) for doc, _score in results]
    sources = ["source1", "source2"]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    logger.info(formatted_response)


if __name__ == "__main__":
    main()
