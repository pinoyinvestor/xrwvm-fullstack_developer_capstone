from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('dealer/<int:dealer_id>/', TemplateView.as_view(template_name="index.html")),  # Route for a single dealer
    path('dealers/', TemplateView.as_view(template_name="index.html")),
    path('register/', TemplateView.as_view(template_name="index.html")),
    path('admin/', admin.site.urls),
    path('djangoapp/', include('djangoapp.urls')),  # Include URLs from djangoapp
    path('login/', TemplateView.as_view(template_name="index.html")),  # React app login
    path('about/', TemplateView.as_view(template_name="About.html")),  # About page
    path('postreview/<int:dealer_id>/', TemplateView.as_view(template_name="index.html")),  # Route for posting a review
    path('', TemplateView.as_view(template_name="Home.html")),  # Home page
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
