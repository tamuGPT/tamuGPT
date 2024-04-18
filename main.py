import argparse
import logging

from config import AppConfig
from src.database import Database
from src.language_models.language_model import LanguageModel

logger = logging.getLogger(__name__)


def main():
    config = AppConfig()

    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    db = Database(config.DATABASE_PATH)

    results = db.search(query_text)
    if len(results) == 0 or results[0][1] < 0.7:
        logger.info(f"Unable to find matching results.")
        return

    # extract context text
    context_text = "\n\n---\n\n".join(
        [doc.page_content for doc, _score in results])

    model = LanguageModel(config.TEMPLATE_PATH)
    prompt = model.generate_prompt(context_text, query_text)
    response_text = model.predict(prompt)

    # get sources
    sources = [doc.metadata.get("source", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    logger.info(formatted_response)


if __name__ == "__main__":
    main()
