import json
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing.sequence import pad_sequences


def generate_text(input_text):
    next_words = 10
    max_words_to_be_considered = 7
    model_path = 'data/word_generator.tf'
    tokenizer_path = 'data/tokenizer.json'

    model = load_model(model_path)
    with open(tokenizer_path) as f:
        data = json.load(f)
        tokenizer = tokenizer_from_json(data)

    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([input_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_words_to_be_considered - 1, padding='pre')
        predicted_probs = model.predict(token_list, verbose=0)

        predicted_index = np.argmax(predicted_probs, axis=-1)

        output_word = ""
        for word, index in tokenizer.word_index.items():
            if index == predicted_index:
                output_word = word
                break
        input_text += " " + output_word
    return input_text
