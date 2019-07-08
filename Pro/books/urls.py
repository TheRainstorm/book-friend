from django.urls import path
from books import views

urlpatterns = [
    path('', views.go2index, name='go2index'),
    path('index/', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('delete/<int:book_id>/',views.delete),
    path('goupdate/<int:book_id>/',views.goupdate),
    path('update/',views.update),
    path('<int:book_id>',views.detail),
    path('types/<int:type_id>',views.types),
    path('download/<int:book_id>',views.filedownload),
    path('paihang/',views.paihang),
]