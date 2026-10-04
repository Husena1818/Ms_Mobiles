from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("book-repair/", views.book_repair, name="book_repair"),
    path("repair-track/", views.repair_tracking, name="repair_tracking"),
]