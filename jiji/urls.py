from django.urls import path
from .views import ask_jiji

urlpatterns = [
    path("ask-jiji", ask_jiji),
]
