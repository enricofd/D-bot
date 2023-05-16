import json
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


def load_data(file_path):
    with open(file_path, "r") as f:
        data_raw = json.load(f)
    return [value[1] for value in data_raw.values()]


def save_tokenizer(tokenizer, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(tokenizer.to_json(), ensure_ascii=False))


def create_input_sequences(data, tokenizer):
    input_sequences = []
    for line in data:
        token_list = tokenizer.texts_to_sequences([line])[0]
        for i in range(1, len(token_list)):
            n_gram_sequence = token_list[:i + 1]
            input_sequences.append(n_gram_sequence)
    return input_sequences


def build_model(total_words, max_words_to_be_considered):
    model = Sequential()
    model.add(Embedding(total_words, 64, input_length=max_words_to_be_considered - 1))
    model.add(LSTM(150))
    model.add(Dense(total_words, activation='softmax'))
    model.compile(loss='sparse_categorical_crossentropy', optimizer=Adam(lr=0.01))
    return model


def main_generator():
    data = load_data("data/data_raw.json")

    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(data)
    save_tokenizer(tokenizer, 'data/tokenizer.json')

    input_sequences = create_input_sequences(data, tokenizer)
    max_words_to_be_considered = 7
    total_words = len(tokenizer.word_index) + 1

    input_sequences = np.array(pad_sequences(input_sequences, maxlen=max_words_to_be_considered))
    x, y = input_sequences[:, :-1], input_sequences[:, -1]

    model = build_model(total_words, max_words_to_be_considered)
    model.fit(x, y, epochs=100, verbose=0)
    model.save('data/word_generator.tf')
