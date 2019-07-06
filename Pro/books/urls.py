from django.urls import path
from books import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('delete/<int:book_id>/',views.delete),
    path('goupdate/<int:book_id>/',views.goupdate),
    path('update/',views.update),
    path('<int:book_id>',views.detail),
]