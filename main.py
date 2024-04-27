import os
import argparse
import logging
import logging.config
import nltk


from config import AppConfig
from src.database import Database
from src.language_models.openai_language_model import OpenAILanguageModel
from google_search import google_custom_search_engine
from src.search.summarize_with_llm import summarize_search_results_with_llm
from src.search.rank_with_llm import rank_results_with_llm

logger = logging.getLogger(__name__)


def main():
    config = AppConfig(log_level="INFO")
    logging.config.dictConfig(config.logging_config)

    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    logger.info(f"Query text: {query_text}")

    logger.info(f"Searching for query using google search: {query_text}")
    search_results = google_custom_search_engine(query_text)
    logger.info(f"Retrieved {len(search_results)} results.")

    # db = Database(config.DATABASE_PATH)

    # results = db.search(query_text)
    # if len(results) == 0 or results[0][1] < 0.7:
    #     logger.info(f"Unable to find matching results.")
    #     return

    # extract context text
    # context_text = "\n\n---\n\n".join(
    #     [doc.page_content for doc, _score in results])

    context_text, context_text_array, cleaned_search_results, urls = summarize_search_results_with_llm(
        config, query_text, search_results)
    logger.info(f"Length of processed search context: {len(context_text)}")

    ranked_content, ranked_urls = rank_results_with_llm(
        config, query_text, context_text_array, cleaned_search_results, urls)

    logger.info(f"Length of Ranked Content: {len(ranked_content)}")

    model = OpenAILanguageModel(config.TEMPLATE_PATH)
    # prompt = model.generate_prompt(context_text, query_text)

    words = ranked_content.split()
    # Slice to get the first 3000 words
    first_3900_words = words[:3000]

    context = ' '.join(first_3900_words)
    prompt = model.generate_prompt(context=context, question=query_text)
    query_response = model.invoke(prompt)
    logger.info(f"\nQuery Response: {query_response}")

    print("\n\n\n")
    logger.info(f"Query: {query_text}")
    logger.info(f"Response: {query_response.content}")
    logger.info(f"Sources:")
    for url in ranked_urls:
        logger.info(f"{url}")


if __name__ == "__main__":
    main()
