import os
import requests
import json


def search(search_value: str = None) -> str:

    WEB_SEARCH_KEY = os.environ.get("WEB_SEARCH_KEY")

    if search_value:
        try:
            url = "https://contextualwebsearch-websearch-v1.p.rapidapi.com/api/Search/WebSearchAPI"

            querystring = {
                "q": search_value,
                "pageNumber": "1",
                "pageSize": "10",
                "autoCorrect": "true",
            }

            headers = {
                "X-RapidAPI-Key": WEB_SEARCH_KEY,
                "X-RapidAPI-Host": (
                    "contextualwebsearch-websearch-v1.p.rapidapi.com"
                ),
            }

            response = requests.request(
                "GET", url, headers=headers, params=querystring
            )

            response_dict = json.loads(response.text)

            final_response = [
                result["url"] for result in response_dict["value"][:3]
            ]

            return final_response

        except:
            return "API error."

    else:
        return "Could not identify value to search."
