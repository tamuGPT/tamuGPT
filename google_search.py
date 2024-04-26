from googlesearch import search
from serpapi import GoogleSearch
from config import AppConfig
import requests
from bs4 import BeautifulSoup
import json
import os

config = AppConfig()


def get_relevant_links(query, no_results):

    # set query to search for in Google
    query = "TAMU Spring Graduation Ceremony 2024"

    # execute query and store search results
    results = search(query, num_results=no_results)

    print("\nRetrieved results\n")
    # iterate over all search results and print them
    for result in results:
        print(result)

#SERPAPI Google Search API
def serpapi(query):
    params = {
    "q": query,
    "hl": "en",
    "gl": "us",
    "api_key": config.GOOGLE_SEARCH_API_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    answer_box = results["answer_box"]
    print("\nRetrieved results\n")
    print(answer_box)

def scrape_content(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve {url}")
        return {'content': '', 'error': f"Failed to retrieve {url}"}

    content = response.text

    # Save HTML content to a file
    # filename = f"scraped_html_files/{url.replace('/', '_').replace(':', '_').replace('.', '_')}.html"
    # with open(filename, 'w', encoding='utf-8') as f:
    #     f.write(content)

    return {'content': content}

def save_as_html(results):
    html_content = "<html>\n<head>\n<title>Search Results</title>\n</head>\n<body>\n"
    
    for result in results:
        html_content += f"<h2><a href='{result['url']}'>{result['title']}</a></h2>\n"
        html_content += f"<p>{result['description']}</p>\n"
        html_content += f"<p><strong>Metadata:</strong><br>{result['metadata']}</p>\n"
        html_content += "<hr>\n"
    
    html_content += "</body>\n</html>"
    
    with open('search_results.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("\n\nSearch results saved in search_results.html")

def google_custom_search_engine(query):
    # get the API KEY here: https://developers.google.com/custom-search/v1/overview
    API_KEY = config.GOOGLE_CSE_API_KEY
    # get your Search Engine ID on your CSE control panel
    SEARCH_ENGINE_ID = config.GOOGLE_CSE_ID

    # using the first page
    page = 1
    # constructing the URL
    # doc: https://developers.google.com/custom-search/v1/using_rest
    # calculating start, (page=2) => (start=11), (page=3) => (start=21)
    start = (page - 1) * 10 + 1
    url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}"

    # make the API request
    data = requests.get(url).json()

    # Check if search was successful
    if 'items' not in data:
        print("No search results found.")
        return

    results = []

    for item in data['items']:
        url = item['link']
        metadata = scrape_content(url)
        
        result = {
            'url': url,
            'title': item['title'],
            'description': item.get('snippet', ''),
            'metadata': metadata
        }
        
        results.append(result)

    save_as_html(results)

    document = "search_results.html"
    # content = load_document(document)
    # print("content\n",content)
    # Store results in a JSON file
    # with open('search_results.json', 'w', encoding='utf-8') as f:
    #     json.dump(results, f, ensure_ascii=False, indent=4)

    # print("\n\nScraped results stored in search_results.json")

if __name__=="__main__":

    query = "TAMU Spring Graduation Ceremony 2024"

    no_results = 1
    print("\nGetting {} relevant link{} through google search .......".format(no_results, "s" if no_results!=1 else ""))
    # get_relevant_links(query, no_results)

    query2 = "when does spring break start 2024 in tamu"
    print("\nGetting related answers using SerpAPI .......")
    # serpapi(query2)

    # the search query you want
    # query3 = "TAMU Spring Graduation Ceremony 2024"
    query4 = "What are the Professor James Caverlee's Recent publications?"

    google_custom_search_engine(query4)