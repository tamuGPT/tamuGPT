import logging

from src.language_models.openai_language_model import OpenAILanguageModel
from src.search.data_processor import clean_html, truncate_html_with_nltk

logger = logging.getLogger(__name__)


def summarize_search_results_with_llm(config, query, search_results):
    search_results = search_results[:7]
    summarized_context_string = ""
    filtered_results = []

    for result_item in search_results:
        html_content = result_item["metadata"]["content"]
        cleaned_html = clean_html(html_content)
        truncated_html = truncate_html_with_nltk(cleaned_html, 5000)
        logger.info(f"Length of cleaned html: {len(truncated_html.split())}")

        summarization_model = OpenAILanguageModel(config.SUMMARY_TEMPLATE_PATH)
        summary_prompt = summarization_model.generate_prompt(
            context=truncated_html, question=query)
        response = summarization_model.invoke(summary_prompt)

        logger.info(f"Summarization Response: {response}")
        logger.info(f"Length of summarization response content: "
                    f"{len(response.content)}\n\n\n")

        result_item['truncated_html'] = truncated_html
        result_item['llm_summary'] = response.content
        summarized_context_string += response.content

        filtered_results.append(result_item)

    return filtered_results, summarized_context_string
