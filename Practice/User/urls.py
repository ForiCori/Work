from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.UserLogin.as_view(), name='login'),
    path('registration/', views.UserRegistration.as_view(), name='registration'),
    path('logout/', views.logout_page, name='logout')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
