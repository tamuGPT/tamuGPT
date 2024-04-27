import logging

from src.language_models.openai_language_model import OpenAILanguageModel
from src.search.data_processor import clean_html, truncate_html_with_nltk

logger = logging.getLogger(__name__)


def summarize_search_results_with_llm(config, query, results):
    results = results[:7]
    cleaned_results = ""
    cleaned_result_array = []
    cleaned_search_results = []
    for res in results:
        html_content = res["metadata"]["content"]
        cleaned_html = clean_html(html_content)
        cleaned_html = truncate_html_with_nltk(cleaned_html, 5000)
        logger.info("Length of cleaned html: %d", len(cleaned_html.split()))
        # words = cleaned_html.split()
        # middle_index = len(words) // 2
        # start_index = max(0, middle_index - 1000)
        # end_index = min(len(words), middle_index + 1000)
        # middle_2000_words = ' '.join(words[start_index:end_index])
        # cleaned_results += middle_2000_words

        summarization_model = OpenAILanguageModel(config.SUMMARY_TEMPLATE_PATH)
        summary_prompt = summarization_model.generate_summary_prompt(
            cleaned_html, query)
        response = summarization_model.invoke(summary_prompt)
        logger.info(f"\nResponse: {response}")
        logger.info(f"\nResponse Content: {response.content}")
        logger.info(f"Length of response content: "
                    f"{len(response.content)}\n\n\n")
        cleaned_results += response.content
        cleaned_result_array.append(response.content)
        cleaned_search_results.append(cleaned_html)

    return cleaned_results, cleaned_result_array, cleaned_search_results
