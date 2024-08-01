from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review

logger = logging.getLogger(__name__)

@login_required
def add_review(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            response = post_review(data)
            if response and response.get('status') == 'success':
                return JsonResponse({"status": 200,
                                     "message": "Review posted successfully"})
            else:
                return JsonResponse({"status": 500,
                                     "message": "Error in posting review"},
                                    status=500)
        except json.JSONDecodeError:
            return JsonResponse({"status": 400,
                                 "message": "Invalid JSON format"},
                                status=400)
        except Exception as e:
            return JsonResponse({"status": 500, "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": 405, "message": "Method not allowed"},
                            status=405)

def get_dealerships(request, state="All"):
    endpoint = "/fetchDealers" if state == "All" else f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    if dealerships is None:
        logger.error(f"Failed to retrieve dealerships from endpoint: {endpoint}")
        return JsonResponse({"status": 500,
                             "message": "Error fetching dealerships"},
                            status=500)
    return JsonResponse({"status": 200, "dealers": dealerships})

def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{dealer_id}"
        reviews = get_request(endpoint)
        if reviews is None:
            return JsonResponse({"status": 500,
                                 "message": "Error fetching dealer reviews"},
                                status=500)
        for review in reviews:
            review_text = review.get('review', '')
            sentiment_response = analyze_review_sentiments(review_text)
            review['sentiment'] = sentiment_response.get('sentiment',
                                                         'Unknown') if sentiment_response else 'Unknown'
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"}, status=400)

def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        dealership = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealership})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')
            if not username or not password:
                response_data = {"status": "Failed",
                                 "message": "Username and password are required"}
                logger.warning("Login attempt with missing username or password.")
                return JsonResponse(response_data)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                response_data = {"userName": username, "status": "Authenticated"}
                logger.info(f"User {username} authenticated successfully.")
            else:
                response_data = {"userName": username, "status": "Failed",
                                 "message": "Invalid credentials"}
                logger.warning(f"Invalid login attempt for user {username}.")
        except json.JSONDecodeError:
            response_data = {"status": "Failed", "message": "Invalid request format"}
            logger.error("Error decoding JSON from request body.")
        except Exception as e:
            response_data = {"status": "Failed", "message": str(e)}
            logger.error(f"Unexpected error during login: {str(e)}")
    else:
        response_data = {"status": "Failed", "message": "Only POST method is allowed"}
        logger.warning("Login attempt with non-POST method.")
    return JsonResponse(response_data)

@csrf_exempt
def logout_user(request):
    if request.method == 'GET':
        try:
            if request.user.is_authenticated:
                username = request.user.username
                logout(request)
                response_data = {"userName": username}
                logger.info(f"User {username} logged out successfully.")
                return JsonResponse(response_data)
            else:
                response_data = {"status": "Failed", "message": "No user is logged in"}
                logger.warning("Logout attempt with no authenticated user.")
                return JsonResponse(response_data, status=400)
        except Exception as e:
            response_data = {"status": "Failed", "message": str(e)}
            logger.error(f"Unexpected error during logout: {str(e)}")
            return JsonResponse(response_data, status=500)
    else:
        response_data = {"status": "Failed", "message": "Only GET method is allowed"}
        logger.warning("Logout attempt with non-GET method.")
        return JsonResponse(response_data, status=405)

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')
            first_name = data.get('firstName')
            last_name = data.get('lastName')
            email = data.get('email')
            if not username or not password or not email:
                response_data = {"status": "Failed",
                                 "message": "Username, password, and email are required"}
                logger.warning("Registration attempt with missing fields.")
                return JsonResponse(response_data)
            if User.objects.filter(username=username).exists():
                response_data = {"status": "Failed", "error": "Already Registered"}
                logger.warning(f"Registration attempt with already existing username: {username}")
                return JsonResponse(response_data)
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            login(request, user)
            response_data = {"userName": username, "status": "Registered"}
            logger.info(f"User {username} registered and logged in successfully.")
        except json.JSONDecodeError:
            response_data = {"status": "Failed", "message": "Invalid request format"}
            logger.error("Error decoding JSON from request body.")
        except Exception as e:
            response_data = {"status": "Failed", "message": str(e)}
            logger.error(f"Unexpected error during registration: {str(e)}")
    else:
        response_data = {"status": "Failed", "message": "Only POST method is allowed"}
        logger.warning("Registration attempt with non-POST method.")
    return JsonResponse(response_data)

def get_cars(request):
    count = CarMake.objects.filter().count()
    if count == 0:
        initiate()  # Call initiate to populate the database if empty
    car_models = CarModel.objects.select_related('car_make')
    cars = [{"CarModel": car_model.name, "CarMake": car_model.car_make.name}
            for car_model in car_models]
    return JsonResponse({"CarModels": cars})
