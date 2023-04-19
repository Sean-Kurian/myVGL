from django.db import models
from django.utils.text import slugify

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Game.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = f"{slug}-{qs.first().id}"
        return create_slug(instance, new_slug=new_slug)
    return slug

class Publisher(models.Model):
    name = models.CharField(max_length=255)

class Developer(models.Model):
    name = models.CharField(max_length=255)

class Genre(models.Model):
    name = models.CharField(max_length=255)

class Platform(models.Model):
    name = models.CharField(max_length=255)

class User(models.Model):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)

class Game(models.Model):
    title = models.CharField(max_length=255)
    release_date = models.DateField()
    summary = models.TextField()
    publishers = models.ManyToManyField(Publisher)
    developers = models.ManyToManyField(Developer)
    platforms = models.ManyToManyField(Platform)
    genres = models.ManyToManyField(Genre)
    slug = models.SlugField(unique=True, blank=True, max_length = 255)

    @property
    def average_rating(self):
        ratings = Rating.objects.filter(game=self)
        if ratings.exists():
            return round(ratings.aggregate(models.Avg('score'))['score__avg'], 2)
        else:
            return None
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_slug(self)
        super(Game, self).save(*args, **kwargs)

class Rating(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()

class Like(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)

class Comment(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers', null=True)

class Thumbnail(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='thumbnails')
    image = models.ImageField(upload_to='thumbnails')