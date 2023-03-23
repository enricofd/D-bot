from web_crawl import crawl
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem import WordNetLemmatizer
import re
import json
import nltk

nltk.download('wordnet')

def save_data(urls_to_crawl: list) -> None:

    # try:
    lemmatizer = WordNetLemmatizer()
    vectorizer = TfidfVectorizer()

    print(urls_to_crawl)

    searched_urls, result = crawl(urls_to_crawl)
    titles, texts = zip(*result)

    j = [re.findall('\w+', text) for text in texts]

    texts_processed = [" ".join([lemmatizer.lemmatize(word) for word in re.findall('\w+', text)]) for text in texts]

    try:  
        with open('data/data_raw.json', 'r') as f:
            data_raw = json.load(f)

        raw_titles, raw_urls, raw_texts = zip(*[(value[0], key, value[1]) for key, value in data_raw.items()])

    except:
        raw_titles, raw_urls, raw_texts = [], [], []

    titles = list(titles)

    urls_to_crawl.extend(raw_urls)
    titles.extend(raw_titles)
    texts_processed.extend(raw_texts)

    tfidf = vectorizer.fit_transform(texts_processed).toarray()

    data_new = {term: {title: value for title, value in zip(titles, tfidf_value)} for term, tfidf_value in zip(vectorizer.get_feature_names_out(), tfidf.T)}
    title_url_new = {title: url for title, url in zip(titles, urls_to_crawl)}

    # --- Update data --- 

    try:
        with open('data/data.json', 'r') as f:
            data = json.load(f)

        with open('data/title_url.json', 'r') as f:
            title_url = json.load(f)

        data.update(data_new)
        title_url.update(title_url_new)

    except:
        data = data_new
        title_url = title_url_new

    with open('data/data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

    with open('data/title_url.json', 'w', encoding='utf-8') as f:
        json.dump(title_url, f, ensure_ascii=False)

    data_raw = {url: (title, text) for title, url, text in zip(titles, urls_to_crawl, texts_processed)}

    with open('data/data_raw.json', 'w', encoding='utf-8') as f:
        json.dump(data_raw, f, ensure_ascii=False)

    return len(searched_urls)

    # except:

    #     return 0
