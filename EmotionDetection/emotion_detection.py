import requests
import json

def emotion_detector(text_to_analyze):
    # Define the URL for the emotion analysis API
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'

    # Create the payload with the text to be analyzed
    myobj = { "raw_document": { "text": text_to_analyze } }

    # Set the headers with the required model ID for the API
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}

    # Make a POST request to the API with the payload and headers
    response = requests.post(url, json=myobj, headers=header)
    
    result = {}
    # Check data validity
    if response.status_code == 400:
        # Construct the result
        result["anger"] = None
        result["disgust"] = None
        result["fear"] = None
        result["joy"] = None
        result["sadness"] = None
        result["dominant_emotion"] = None
    elif response.status_code == 200:
        # Parse the response from the API
        formatted_response = json.loads(response.text)

        # Find the dominant emotion
        emotions = formatted_response["emotionPredictions"][0]["emotion"]
        dominant_emotion = {"emotion": "", "score": 0.0}
        for key, value in emotions.items():
            if value > dominant_emotion["score"]:
                dominant_emotion["emotion"] = key
                dominant_emotion["score"] = value
        
        # Construct the result
        result["anger"] = emotions["anger"]
        result["disgust"] = emotions["disgust"]
        result["fear"] = emotions["fear"]
        result["joy"] = emotions["joy"]
        result["sadness"] = emotions["sadness"]
        result["dominant_emotion"] = dominant_emotion["emotion"]
    
    return result
