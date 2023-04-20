from rest_framework import generics
from .models import Game
from .serializers import GameSerializer

class GameListView(generics.ListCreateAPIView):
    queryset = Game.objects.all()
    serializer_class = GameSerializer