from django.urls import path
from collects import views

urlpatterns = [
    path('collect_add/<int:book_id>',views.collect_add),
    path('collect_del/<int:book_id>',views.collect_del),
]