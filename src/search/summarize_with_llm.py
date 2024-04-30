import logging

from src.language_models.openai_language_model import OpenAILanguageModel
from src.search.data_processor import clean_html, truncate_html_with_nltk

from tqdm import tqdm

logger = logging.getLogger(__name__)


def summarize_search_results_with_llm(config, query, search_results):
    search_results = search_results[:7]
    summarized_context_string = ""
    filtered_results = []

    print("\n")
    logger.info("Picking relevant content from search results..")
    for result_item in tqdm(search_results):
        html_content = result_item["metadata"]["content"]
        cleaned_html = clean_html(html_content)
        truncated_html = truncate_html_with_nltk(cleaned_html, 5000)
        logger.debug(f"Length of cleaned html: {len(truncated_html.split())}")

        summarization_model = OpenAILanguageModel(config.SUMMARY_TEMPLATE_PATH)
        summary_prompt = summarization_model.generate_prompt(
            context=truncated_html, question=query)
        try:
            response = summarization_model.invoke(summary_prompt)

            logger.debug(f"Summarization Response: {response}")
            logger.debug(f"Length of summarization response content: "
                         f"{len(response.content)}\n\n\n")

            result_item['truncated_html'] = truncated_html
            result_item['llm_summary'] = response.content
            summarized_context_string += response.content
        except Exception as e:
            result_item['truncated_html'] = ""
            result_item['llm_summary'] = ""

        filtered_results.append(result_item)

    logger.debug(f"Length of processed search context: "
                 f"{len(summarized_context_string)}")

    return filtered_results, summarized_context_string
