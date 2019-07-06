from django.urls import path
from users import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('ajax/check_account/<str:user_name>/', views.check_account, name='check_account'),
]