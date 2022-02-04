from django.contrib import admin
from .models import Category, Video, VideoReview, VideoPlay

admin.site.register(Category)
admin.site.register(Video)
admin.site.register(VideoPlay)
admin.site.register(VideoReview)


