from typing import Dict, Any

from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import re
import json


def local_similarity_search(query: str, th: float = 0) -> list:
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

        max_word_similarity = 0
        max_data_word_similarity = ""

        for data_word in data.keys():
            try:
                syns1 = wordnet.synsets(word)[0]
                syns2 = wordnet.synsets(data_word)[0]

                path_similarity = syns1.path_similarity(syns2)
                wup_similarity = syns1.wup_similarity(syns2)

                total_similarity = (path_similarity + wup_similarity) / 2

                if total_similarity > max_word_similarity:
                    max_word_similarity = total_similarity
                    max_data_word_similarity = data_word

            except:
                pass

        if max_word_similarity > 0:
            for doc in data[max_data_word_similarity].keys():

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
