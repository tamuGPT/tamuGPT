import logging
import re
from src.language_models.openai_language_model import OpenAILanguageModel

logger = logging.getLogger(__name__)


def rank_results_with_llm(config, query_text, search_results):
    rank_input_text = ""

    ranked_summary_list = []
    ranked_search_results = []

    for idx, result_item in enumerate(search_results):
        result_llm_summary = result_item["llm_summary"]
        rank_input_text += f"Text {idx + 1}: \n{result_llm_summary}\n\n"

    ranking_model = OpenAILanguageModel(config.RANK_TEMPLATE_PATH)
    ranking_prompt = ranking_model.generate_prompt(
        context=rank_input_text, question=query_text)

    response = ranking_model.invoke(ranking_prompt)
    logger.info(f"\nRanked Response: {response.content}")

    pattern = r'\[(.*?)\]'
    match = re.search(pattern, response.content)
    if match:
        rank_order_string = match.group(1)
    else:
        return search_results, ''.join(ranked_summary_list)

    rank_order_list = rank_order_string.split(",")

    for i in range(len(rank_order_list)):
        pattern = r'\d+'  # Match any digit
        results = re.findall(pattern, rank_order_list[i])
        rank_order_list[i] = ''.join(results)
        rank = int(rank_order_list[i])
        ranked_summary_list.append(search_results[rank-1]["truncated_html"])
        ranked_search_results.append(search_results[rank-1])

    return ranked_search_results, ''.join(ranked_summary_list),
