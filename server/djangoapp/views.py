from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from .models import CarMake, CarModel
from .populate import initiate  # Importera initiate-funktionen

# Get an instance of a logger
logger = logging.getLogger(__name__)

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')
            
            if not username or not password:
                response_data = {"status": "Failed", "message": "Username and password are required"}
                logger.warning("Login attempt with missing username or password.")
                return JsonResponse(response_data)
            
            # Authenticate the user
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                response_data = {"userName": username, "status": "Authenticated"}
                logger.info(f"User {username} authenticated successfully.")
            else:
                response_data = {"userName": username, "status": "Failed", "message": "Invalid credentials"}
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
            else:
                response_data = {"status": "Failed", "message": "No user is logged in"}
                logger.warning("Logout attempt with no authenticated user.")
        except Exception as e:
            response_data = {"status": "Failed", "message": str(e)}
            logger.error(f"Unexpected error during logout: {str(e)}")
    else:
        response_data = {"status": "Failed", "message": "Only GET method is allowed"}
        logger.warning("Logout attempt with non-GET method.")
    
    return JsonResponse(response_data)

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
                response_data = {"status": "Failed", "message": "Username, password, and email are required"}
                logger.warning("Registration attempt with missing fields.")
                return JsonResponse(response_data)

            # Check if the user already exists
            if User.objects.filter(username=username).exists():
                response_data = {"status": "Failed", "error": "Already Registered"}
                logger.warning(f"Registration attempt with already existing username: {username}")
                return JsonResponse(response_data)

            # Create a new user
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            
            # Log in the user
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
        initiate()  # Anropa initiate för att fylla databasen om den är tom
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels": cars})
