from rest_framework import serializers
from .models import Game, Publisher, Developer, Genre, Platform

class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = ('id', 'name')

class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Developer
        fields = ('id', 'name')

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name')

class PlatformSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platform
        fields = ('id', 'name')

class GameSerializer(serializers.ModelSerializer):
    publishers = PublisherSerializer(many=True)
    developers = DeveloperSerializer(many=True)
    genres = GenreSerializer(many=True)
    platforms = PlatformSerializer(many=True)

    class Meta:
        model = Game
        fields = ('id', 'title', 'release_date', 'summary', 'publishers', 'developers', 'genres', 'platforms', 'slug')