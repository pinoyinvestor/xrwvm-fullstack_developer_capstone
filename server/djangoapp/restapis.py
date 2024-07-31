import os
import requests
from dotenv import load_dotenv

# Ladda miljövariabler från .env-fil
load_dotenv()

# Backend URL och Sentiment Analyzer URL från miljövariabler
backend_url = os.getenv('backend_url', default="https://danielhedenb-3030.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai")
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default="http://localhost:5050/")

def get_request(endpoint, **kwargs):
    # Bygg query-string från kwargs
    params = "&".join(f"{key}={value}" for key, value in kwargs.items())
    
    # Bygg URL med query-string
    request_url = f"{backend_url}{endpoint}?{params}"
    print(f"GET from {request_url}")
    
    try:
        # Gör GET-anrop till URL:en
        response = requests.get(request_url)
        # Kontrollera om anropet lyckades
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        # Hantera alla nätverks- eller HTTP-fel
        print(f"Network exception occurred: {e}")
        return None

def analyze_review_sentiments(text):
    # URL för sentimentanalys
    request_url = f"{sentiment_analyzer_url}analyze/{text}"
    print(f"GET from {request_url}")

    try:
        # Gör GET-anrop till sentimentanalys URL:en
        response = requests.get(request_url)
        # Kontrollera om anropet lyckades
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        # Hantera alla nätverks- eller HTTP-fel
        print(f"Network exception occurred: {e}")
        return None

def post_review(data_dict):
    # URL för att posta en recension
    request_url = f"{backend_url}reviews"
    print(f"POST to {request_url} with data {data_dict}")

    try:
        # Gör POST-anrop med data
        response = requests.post(request_url, json=data_dict)
        # Kontrollera om anropet lyckades
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        # Hantera alla nätverks- eller HTTP-fel
        print(f"Network exception occurred: {e}")
        return None
