import os
import requests
from dotenv import load_dotenv
import logging

# Konfigurera loggning
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Ladda miljövariabler från .env-fil
load_dotenv()


# Backend URL och Sentiment Analyzer URL från miljövariabler
backend_url = os.getenv(
    'BACKEND_URL',
    "https://danielhedenb-3030.theiadockernext-1-labs-prod-theiak8s-4-"
    "tor01.proxy.cognitiveclass.ai"
)
sentiment_analyzer_url = os.getenv(
    'SENTIMENT_ANALYZER_URL',
    "https://sentianalyzer.1k348mhoailo.us-south.codeengine.appdomain."
    "cloud"
)

def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params = params + key + "=" + value + "&"
    
    request_url = backend_url + endpoint + "?" + params

    print("GET from {} ".format(request_url))
    try:
        # Anropar get-metoden i requests-biblioteket med URL och parametrar
        response = requests.get(request_url)
        return response.json()
    except:
        # Om något fel inträffar
        print("Network exception occurred")
    finally:
        print("GET request call complete!")




def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url+"analyze/"+text
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")


def post_review(data_dict):
    request_url = backend_url+"/insert_review"
    try:
        response = requests.post(request_url,json=data_dict)
        print(response.json())
        return response.json()
    except:
        print("Network exception occurred")