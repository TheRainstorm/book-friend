from django.urls import path
from users import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout, name='register'),
    path('home/', views.home),    
    path('ajax/check_account/<str:user_name>/', views.check_account, name='check_account'),
    path('recent_read/',views.recent_read),
    path('edit_info/', views.edit_info),    
    path('personal_comments/', views.personal_comments),    
    path('my_collects/', views.my_collects),
    path('get_headpic/', views.get_headpic),
    path('home/add/', views.shangchuan),
]