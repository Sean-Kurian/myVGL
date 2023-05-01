from django.urls import path
from . import views

urlpatterns = [
    path('api/game/', views.GameListView.as_view()),
]