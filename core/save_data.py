from typing import Tuple

from web_crawl import crawl
from classify import classify
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import WordNetLemmatizer
import re
import json
import nltk

nltk.download("wordnet")


def save_data(urls_to_crawl: list) -> tuple[int, int] | int:
    try:
        lemmatizer = WordNetLemmatizer()
        vectorizer = TfidfVectorizer()

        searched_urls, result = crawl(urls_to_crawl)
        titles, texts = zip(*result)
        positivity_list = classify(texts)

        texts_processed = [
            " ".join(
                [
                    lemmatizer.lemmatize(word)
                    for word in re.findall("\w+", text)
                ]
            )
            for text in texts
        ]

        try:
            with open("data/data_raw.json", "r") as f:
                data_raw = json.load(f)

            raw_titles, raw_urls, raw_texts, raw_positivity_list = zip(
                *[(value[0], key, value[1], value[2]) for key, value in data_raw.items()]
            )

        except:
            raw_titles, raw_urls, raw_texts, raw_positivity_list = [], [], [], []

        searched_urls = list(searched_urls)
        titles = list(titles)

        searched_urls.extend(raw_urls)
        titles.extend(raw_titles)
        positivity_list.extend(raw_positivity_list)
        texts_processed.extend(raw_texts)

        tfidf = vectorizer.fit_transform(texts_processed).toarray()

        data_new = {
            term: {title: value for title, value in zip(titles, tfidf_value)}
            for term, tfidf_value in zip(
                vectorizer.get_feature_names_out(), tfidf.T
            )
        }

        title_url_new = {
            title: url for title, url in zip(titles, searched_urls)
        }

        title_positivity_new = {
            title: positivity for title, positivity in zip(titles, positivity_list)
        }

        # --- Update data ---

        with open("data/data.json", "w", encoding="utf-8") as f:
            json.dump(data_new, f, ensure_ascii=False)

        with open("data/title_url.json", "w", encoding="utf-8") as f:
            json.dump(title_url_new, f, ensure_ascii=False)

        with open("data/title_positivity.json", "w", encoding="utf-8") as f:
            json.dump(title_positivity_new, f, ensure_ascii=False)

        data_raw = {
            url: (title, text, positivity)
            for title, url, text, positivity in zip(titles, searched_urls, texts_processed, positivity_list)
        }

        with open("data/data_raw.json", "w", encoding="utf-8") as f:
            json.dump(data_raw, f, ensure_ascii=False)

        return len(searched_urls), len(searched_urls) - len(raw_urls)

    except:

        return 0

