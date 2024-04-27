import logging
import re
from src.language_models.openai_language_model import OpenAILanguageModel
from src.search.data_processor import clean_html, truncate_html_with_nltk

logger = logging.getLogger(__name__)


def rank_results_with_llm(config, query_text, cleaned_result_array, cleaned_search_results):
    rank_input_text = ""

    ranked_order = []

    for i in range(len(cleaned_result_array)):
        rank_input_text += f"Text {i + 1}:\n{cleaned_result_array[i]}\n\n"
    ranking_model = OpenAILanguageModel(config.RANK_TEMPLATE_PATH)
    ranking_prompt = ranking_model.generate_prompt(
        context=rank_input_text, question=query_text)

    response = ranking_model.invoke(ranking_prompt)
    logger.info(f"\nRanked Response: {response.content}")
    pattern = r'\[(.*?)\]'
    match = re.search(pattern, response.content)
    rank_order_string = ""
    if match:
        rank_order_string = match.group(1)
    else:
        return ranked_order

    rank_order_list = rank_order_string.split(",")

    for i in range(len(rank_order_list)):
        pattern = r'\d+'  # Match any digit
        results = re.findall(pattern, rank_order_list[i])
        rank_order_list[i] = ''.join(results)
        rank = int(rank_order_list[i])
        ranked_order.append(cleaned_search_results[rank - 1])
    return ''.join(ranked_order)
