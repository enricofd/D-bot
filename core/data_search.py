from nltk.stem import WordNetLemmatizer
import re
import json


def search(query: str) -> list:

    lemmatizer = WordNetLemmatizer()

    with open('data/data.json', 'r') as f:
        data = json.load(f)

    with open('data/title_url.json', 'r') as f:
        title_url = json.load(f)

    
    result = dict()
    words = [lemmatizer.lemmatize(word) for word in re.findall('\w+', query)]
    
    for word in words:
        
        if word in data.keys():
            for doc in data[word].keys():
                
                if doc not in result.keys():
                    result[doc] = data[word][doc]
                    
                else:
                    result[doc] += data[word][doc]

    return [f"{title}: {title_url[title]}" for title in sorted(result)[:3]]