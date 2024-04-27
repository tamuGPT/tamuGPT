import os
import argparse
import logging
import logging.config

from config import AppConfig
from src.database import Database
from src.language_models.openai_language_model import OpenAILanguageModel
from src.search.data_processor import clean_html, truncate_html_with_nltk
from google_search import google_custom_search_engine


logger = logging.getLogger(__name__)


def main():
    config = AppConfig(log_level="INFO")
    logging.config.dictConfig(config.logging_config)

    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text


    results = google_custom_search_engine(query_text)
    results = results[:3]
    cleaned_results = ""
    for res in results:
        html_content = res["metadata"]["content"]
        cleaned_html = clean_html(html_content)
        cleaned_html = truncate_html_with_nltk(cleaned_html)
        cleaned_results += cleaned_html

    db = Database(config.INDEX_NAME)
    vector_store = db.create_vector_store(cleaned_results)

    context_text = cleaned_results
    logger.info(f"Length of context: {len(context_text)}")

    model = OpenAILanguageModel(config.TEMPLATE_PATH)
    # prompt = model.generate_prompt(context_text, query_text)
    response_text = model.invoke(query_text, vector_store)

    # get sources
    # sources = [doc.metadata.get("source", None) for doc, _score in results]
    sources = ["source1", "source2"]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    logger.info(formatted_response)


if __name__ == "__main__":
    main()
