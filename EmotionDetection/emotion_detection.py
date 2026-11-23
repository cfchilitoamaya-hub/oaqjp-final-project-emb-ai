"""Emotion detection using the Watson NLP EmotionPredict service."""
import json
import requests

URL = ('https://sn-watson-emotion.labs.skills.network/v1/'
       'watson.runtime.nlp.v1/NlpService/EmotionPredict')
HEADERS = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
EMOTIONS = ['anger', 'disgust', 'fear', 'joy', 'sadness']


def emotion_detector(text_to_analyze):
    """Return the scores of the five emotions and the dominant emotion."""
    myobj = {"raw_document": {"text": text_to_analyze}}
    response = requests.post(URL, json=myobj, headers=HEADERS, timeout=30)

    # Blank input: the service answers 400, so every value is None
    if response.status_code == 400:
        result = {emotion: None for emotion in EMOTIONS}
        result['dominant_emotion'] = None
        return result

    formatted_response = json.loads(response.text)
    emotions = formatted_response['emotionPredictions'][0]['emotion']
    result = {emotion: emotions[emotion] for emotion in EMOTIONS}
    result['dominant_emotion'] = max(result, key=result.get)
    return result
