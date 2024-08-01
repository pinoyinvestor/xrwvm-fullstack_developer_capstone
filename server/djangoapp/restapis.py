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
    "https://danielhedenb-3030.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai"
)
sentiment_analyzer_url = os.getenv(
    'SENTIMENT_ANALYZER_URL',
    "https://sentianalyzer.1k348mhoailo.us-south.codeengine.appdomain.cloud"
)


def get_request(endpoint, **kwargs):
    # Bygg query-string från kwargs
    params = "&".join(f"{key}={value}" for key, value in kwargs.items())

    # Bygg URL med query-string
    request_url = f"{backend_url}{endpoint}?{params}"
    logger.info(f"GET from {request_url}")

    try:
        # Gör GET-anrop till URL:en
        response = requests.get(request_url)
        # Kontrollera om anropet lyckades
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        # Hantera alla nätverks- eller HTTP-fel
        logger.error(f"Network exception occurred: {e}")
        return None


def analyze_review_sentiments(text):
    # URL för sentimentanalys
    request_url = f"{sentiment_analyzer_url}analyze/{text}"
    logger.info(f"GET from {request_url}")

    try:
        # Gör GET-anrop till sentimentanalys URL:en
        response = requests.get(request_url)
        # Kontrollera om anropet lyckades
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        # Hantera alla nätverks- eller HTTP-fel
        logger.error(f"Network exception occurred: {e}")
        return None


def post_review(data_dict):
    # URL för att posta en recension
    request_url = f"{backend_url}reviews"
    logger.info(f"POST to {request_url} with data {data_dict}")

    try:
        # Gör POST-anrop med data
        response = requests.post(request_url, json=data_dict)
        # Kontrollera om anropet lyckades
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        # Hantera alla nätverks- eller HTTP-fel
        logger.error(f"Network exception occurred: {e}")
        return None
