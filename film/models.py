from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from likes.models import Like
from account.models import User



class Category(models.Model):
    slug = models.SlugField(max_length=100, primary_key=True)
    name = models.CharField(max_length=150, unique=True)
    def __str__(self):
        return self.name



class Video(models.Model):

    title = models.CharField(max_length=40, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='films')
    rating = models.PositiveSmallIntegerField()
    img = models.ImageField(upload_to='images', null=True)
    description = models.TextField()

    body = models.CharField(max_length=140)
    likes = GenericRelation(Like)

    def __str__(self):
        return self.body

    @property
    def total_likes(self):
        return self.likes.count()


class VideoReview(models.Model):

    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews', null=True)
    text = models.TextField()
    rating = models.PositiveIntegerField(default=1)
    likes = models.PositiveSmallIntegerField(default=0)

class VideoPlay(models.Model):
    film = models.FileField(upload_to='videos', null=True, blank=True,
                             validators=[FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='videos')



