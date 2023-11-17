from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("add", views.add, name="add"),
    path("read/<pk>", views.read, name="read"),
    path("update/<pk>", views.update, name="update"),
    path("delete/<pk>", views.delete, name="delete"),
]
