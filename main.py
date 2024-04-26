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

    summarization_model = OpenAILanguageModel(config.SUMMARY_TEMPLATE_PATH)

    results = google_custom_search_engine(query_text)
    results = results[:3]
    cleaned_results = ""
    for res in results:
        html_content = res["metadata"]["content"]
        cleaned_html = clean_html(html_content)
        cleaned_html = truncate_html_with_nltk(cleaned_html)
        # words = cleaned_html.split()
        # middle_index = len(words) // 2
        # start_index = max(0, middle_index - 1000)
        # end_index = min(len(words), middle_index + 1000)
        # middle_2000_words = ' '.join(words[start_index:end_index])
        # cleaned_results += middle_2000_words
        summary_prompt = summarization_model.generate_summary_prompt(
            cleaned_html, query_text)
        response = summarization_model.invoke(summary_prompt)
        logger.info(f"\nResponse: {response}")
        logger.info(f"\nResponse Content: {response.content}")
        logger.debug(f"Length of response content: {
                     len(response.content)}\n\n\n")
        cleaned_results += response.content

    # db = Database(config.DATABASE_PATH)

    # results = db.search(query_text)
    # if len(results) == 0 or results[0][1] < 0.7:
    #     logger.info(f"Unable to find matching results.")
    #     return

    # extract context text
    # context_text = "\n\n---\n\n".join(
    #     [doc.page_content for doc, _score in results])

    context_text = cleaned_results
    logger.info(f"Length of context: {len(context_text)}")

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
