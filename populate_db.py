import requests
import os
import django
from django.db import transaction
from datetime import datetime
import environ

env = environ.Env()
environ.Env.read_env()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myvgl.settings")
django.setup()

from games.models import Game, Platform, Genre, Publisher, Developer, Thumbnail

# Set up the IGDB API endpoint and parameters
url = "https://api.igdb.com/v4/games"
fields = "name, rating, first_release_date, summary, genres.name, platforms.name, involved_companies.company.name, involved_companies.developer, involved_companies.publisher, cover.url"
order = "rating desc"
where = "rating > 0"
limit = 200
headers = {}

# Go here to get client_id and client_secret: https://dev.twitch.tv/login
# Get the access token
auth_url = "https://id.twitch.tv/oauth2/token"
client_id = env("CLIENT_ID")
client_secret = env("CLIENT_SECRET")
grant_type = "client_credentials"
response = requests.post(auth_url, params={"client_id": client_id, "client_secret": client_secret, "grant_type": grant_type})

if response.status_code == 200:
    access_token = response.json()["access_token"]
    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {access_token}",
    }
# Make the API request
response2 = requests.post(url, headers=headers, data=f"fields {fields}; sort {order}; limit {limit}; where {where};")

# Parse the response and create objects for each game and platform
with transaction.atomic():
    for game_data in response2.json():
    # Check if the game already exists
        game = Game.objects.filter(title=game_data["name"]).first()

        if game:
            # If the game already exists, update its fields
            release_date = game_data.get("first_release_date")
            game.release_date = datetime.fromtimestamp(release_date).strftime("%Y-%m-%d") if release_date else None
            game.summary = game_data.get("summary")
            game.save()
        else:
            # If the game does not exist, create a new game object
            first_release_date = game_data.get("first_release_date")
            if first_release_date:
                release_date = datetime.fromtimestamp(first_release_date).strftime("%Y-%m-%d")
            else:
                release_date = None

            game = Game(
                title=game_data["name"],
                release_date=release_date,
                summary=game_data.get("summary")
            )
            game.save()        
        # Create or update the thumbnail object for the game
        cover_data = game_data.get("cover", {})
        cover_url = cover_data.get("url")
        if cover_url:
            thumbnail, created = Thumbnail.objects.get_or_create(game=game, image=cover_url)

        # Create the developer and publisher objects 
        for company_data in game_data.get("involved_companies", []):
            company_name = company_data.get("company", {}).get("name")
            if company_data.get("developer", False):
                developer, created = Developer.objects.get_or_create(name=company_name)
                game.developers.add(developer)
            elif company_data.get("publisher", False):
                publisher, created = Publisher.objects.get_or_create(name=company_name)
                game.publishers.add(publisher)

        # Create the platform objects
        for platform_data in game_data.get("platforms", []):
            platform, created = Platform.objects.get_or_create(name=platform_data["name"])
            game.platforms.add(platform)

        # Create the genre objects
        for genre_data in game_data.get("genres", []):
            genre, created = Genre.objects.get_or_create(name=genre_data["name"])
            game.genres.add(genre)

transaction.commit()