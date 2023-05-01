from django.urls import path
from django.contrib import admin 
from . import views

urlpatterns = [
    path('api/game/', views.GameListView.as_view()),
    path('admin/', admin.site.urls),
]