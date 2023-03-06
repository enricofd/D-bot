import os
import requests


async def search(search_value: str = None, page_number: str = "1", page_size: str = "10") -> str:

    WEB_SEARCH_KEY = os.environ.get("WEB_SEARCH_KEY")

    if search_value:
        try:
            url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/WebSearchAPI"

            querystring = {"q" : search_value, "pageNumber" : page_number, "pageSize" : page_size, "autoCorrect" : "true"}

            headers = {
                "X-RapidAPI-Key": WEB_SEARCH_KEY,
                "X-RapidAPI-Host": "contextualwebsearch-websearch-v1.p.rapidapi.com"
            }

            response = requests.request("GET", url, headers=headers, params=querystring)

            return response.text

        except:
            return "API error."

    else:
        return "Could not identify value to search."