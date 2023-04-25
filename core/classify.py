from tensorflow import keras


def classify(text_list: list[str]) -> list[str]:
    model = keras.models.load_model('classifier/classifier')
    
    return [str(result[1]) for result in model.predict(text_list)]
