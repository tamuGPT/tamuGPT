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
    config = AppConfig(log_level="DEBUG")
    logging.config.dictConfig(config.logging_config)

    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    logger.info(f"Query text: {query_text}")

    logger.info(f"Searching for query using google search: {query_text}")
    search_results = google_custom_search_engine(query_text)
    logger.info(f"Retrieved {len(search_results)} results.")

    filtered_search_results, summarized_context_string = summarize_search_results_with_llm(
        config, query_text, search_results)
    logger.info(f"Length of processed search context: "
                f"{len(summarized_context_string)}")

    ranked_searched_results, ranked_context_string = rank_results_with_llm(
        config, query_text, filtered_search_results)

    logger.info(f"Length of Ranked Content: {len(ranked_context_string)}")
    words = ranked_context_string.split()
    first_3900_words = words[:3000]
    context = ' '.join(first_3900_words)

    model = OpenAILanguageModel(config.TEMPLATE_PATH)
    prompt = model.generate_prompt(context=context, question=query_text)
    query_response = model.invoke(prompt)
    logger.info(f"\nQuery Response: {query_response}")

    print("\n\n\n")
    logger.info(f"Query: {query_text}")
    logger.info(f"Response: {query_response.content}")
    logger.info(f"Sources: ")
    for idx, search_item in enumerate(ranked_searched_results):
        logger.info(f"{idx+1}. {search_item['url']}")


if __name__ == "__main__":
    main()
