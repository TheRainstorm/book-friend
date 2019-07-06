from django.urls import path
from comments import views

urlpatterns = [
    path('addcom/', views.addcom),
    path('delcom/<str:com_id>', views.delcom),
]