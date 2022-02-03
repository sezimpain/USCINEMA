from django.core.validators import FileExtensionValidator
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from account.models import User


class Category(models.Model):
    slug = models.SlugField(max_length=100, primary_key=True)
    name = models.CharField(max_length=150, unique=True)
    def __str__(self):
        return self.name

class Video(models.Model):
    title = models.CharField(max_length=40, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='films', default=None)
    img = models.ImageField(upload_to='images', null=True)
    description = models.TextField()

    def __str__(self):
        return {self.title}

class VideoPlay(models.Model):
    film = models.FileField(upload_to='videos', null=True, blank=True,
                             validators=[FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='videos')

class VideoReview(models.Model):
    video = models.ForeignKey(Video,
                                on_delete=models.CASCADE,
                                related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='reviews', null=True)
    text = models.TextField()
    rating = models.PositiveIntegerField(default=1, validators=[
            MaxValueValidator(5), MinValueValidator(1)])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
   # def count_rating(self,rating):


