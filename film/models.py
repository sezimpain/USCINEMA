from django.core.validators import FileExtensionValidator
from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=40, unique=True)
    img = models.ImageField(upload_to='images', null=True)
    description = models.TextField()
    video = models.FileField(upload_to='videos', null=True,
                             validators=[FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])])
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return {self.title}

