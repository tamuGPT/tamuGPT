import os

import requests
import json
import logging
import PyPDF2
import io

logger = logging.getLogger(__name__)


def scrape_pdf_content(url):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(response.content))

            # Get the number of pages in the PDF
            num_pages = len(pdf_reader.pages)

            content = ''

            # Iterate over each page and extract the text
            for page_num in range(num_pages):
                page = pdf_reader.pages[page_num]
                content += page.extract_text()

            return {'content': content}
        else:
            logging.error(f"Error downloading PDF from "
                          f"{url}: Status code {response.status_code}")
            return {'error': f"Error downloading PDF: Status code {response.status_code}"}

    except Exception as e:
        logging.error(f"Error scraping PDF content from {url}: {e}")
        return {'error': str(e)}


def scrape_content(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)\
            AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36'}
    logger.info(f"Scraping content from {url}")
    try:
        response = requests.get(url, timeout=5, headers=headers)
    except:
        response = None
    if response is None or response.status_code != 200:
        logger.error(f"Failed to retrieve {url}")
        return {'content': '', 'error': f"Failed to retrieve {url}"}

    content = response.text
    return {'content': content}


def google_custom_search_engine(config, query):
    # get the API KEY here: https://developers.google.com/custom-search/v1/overview
    google_cse_api_key = config.GOOGLE_CSE_API_KEY
    # get your Search Engine ID on your CSE control panel
    search_engine_id = config.GOOGLE_CSE_ID

    # using the first page
    page = 1
    # constructing the URL
    # doc: https://developers.google.com/custom-search/v1/using_rest
    # calculating start, (page=2) => (start=11), (page=3) => (start=21)
    start = (page - 1) * 10 + 1
    url = (f"https://www.googleapis.com/customsearch/v1?"
           f"key={google_cse_api_key}&cx={search_engine_id}&q={query}&start={start}")

    try:
        data = requests.get(url, timeout=5).json()
    except:
        data = {}

    if 'items' not in data:
        print("No search results found.")
        return

    results = []

    for item in data['items']:
        url = item['link']

        if url.lower().endswith('.pdf'):
            metadata = scrape_pdf_content(url)
        else:
            metadata = scrape_content(url)

        if 'error' in metadata:
            continue

        result = {
            'url': url,
            'title': item['title'],
            'description': item.get('snippet', ''),
            'metadata': metadata
        }

        results.append(result)

    with open(os.path.join(config.BASE_PATH, "search_results.json"), 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    logger.info("\n\nScraped results stored in search_results.json")
    return results
