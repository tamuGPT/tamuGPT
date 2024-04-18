from googlesearch import search
from serpapi import GoogleSearch
from config import AppConfig

config = AppConfig()


def get_relevant_links(query, no_results):

    # set query to search for in Google
    query = "TAMU Spring Graduation Ceremony 2024"

    # execute query and store search results
    results = search(query, num_results=no_results)

    # If requesting more than 100 results, googlesearch will send multiple requests to go through the pages. To increase the time between these requests, use sleep_interval:

    # To extract more information, such as the description or the result URL, use an advanced search:
    # results = search(query, sleep_interval=5, num_results=200, advanced=True)
    # Returns a list of SearchResult
    # Properties:
    # - title
    # - url
    # - description

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

if __name__=="__main__":

    query = "TAMU Spring Graduation Ceremony 2024"
    no_results = 1
    print("\nGetting {} relevant link{} through google search .......".format(no_results, "s" if no_results!=1 else ""))
    get_relevant_links(query, no_results)

    query2 = "when does spring break start 2024 in tamu"
    print("\nGetting related answers using SerpAPI .......")
    serpapi(query2)