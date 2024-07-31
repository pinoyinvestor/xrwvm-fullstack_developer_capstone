from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'

urlpatterns = [
    path('get_cars/', views.get_cars, name='get_cars'),
    # Path for user login
         path('login/', views.login_user, name='login'),
    # Path for user logout
    path('logout/', views.logout_user, name='logout'),
     path('register/', views.register_user, name='register'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
