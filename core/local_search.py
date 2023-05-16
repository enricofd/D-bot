from nltk.stem import WordNetLemmatizer
import re
import json


def local_search(query: str, th: float = 0) -> dict:
    lemmatizer = WordNetLemmatizer()

    with open("data/data.json", "r") as f:
        data = json.load(f)

    with open("data/title_url.json", "r") as f:
        title_url = json.load(f)

    with open("data/title_positivity.json", "r") as f:
        title_positivity = json.load(f)

    result = dict()
    words = [lemmatizer.lemmatize(word) for word in re.findall("\w+", query)]

    for word in words:

        word = word.lower()
        if word in data.keys():
            for doc in data[word].keys():

                if doc not in result.keys():
                    result[doc] = data[word][doc]

                else:
                    result[doc] += data[word][doc]

    ordered_result = dict(
        sorted(result.items(), key=lambda item: item[1], reverse=True)
    )

    ordered_result_passed = dict(item for item in ordered_result.items() if float(title_positivity[item[0]]) > th)

    return {
        title: title_url[title] for title in list(ordered_result_passed.keys())[:3]
    }
