import random
from keras.models import load_model

import emotion_detection.preprocessing as pp
import emotion_detection.train as train

def _resolve_emotion(index):
    if index == 0:
        return "joy"
    if index == 1:
        return "anger"
    if index == 2:
        return "love"
    if index == 3:
        return "sadness"
    if index == 4:
        return "fear"
    if index == 5:
        return "surprise"
    return ""

def generate_quote(emotion: str) -> str:
    print(emotion)
    if (emotion == "neutral"):
        return ""
    with open(f'emotion_detection/quotes/{emotion}.txt', 'r', encoding='utf8') as file:
        quotes = file.readlines()
        index = random.randint(0, len(quotes)-1)
        return quotes[index].replace('\n', '')

def _get_model():
    try:
        model = load_model('emotion_detection/model/emotions.h5')
        return model
    except IOError:
        print("Model unavailable on disk. Making the model...")
        model = train.trainModel()
        return model

def predict_emotion(text: str) -> str:
    model = _get_model()
    topredict = list()

    text = pp._normalizeText(text)

    topredict.append(text)
    topredict = pp.textToSequences(topredict)

    result = model.predict(topredict)
    emotion = ""
    max = 0
    ind = -1
    print(result)
    for index, value in enumerate(result[0]):
        if value > max:
            max = value
            ind = index
    if max > 0.95:
        emotion = _resolve_emotion(ind)
        return emotion
    else: 
        return "neutral"
