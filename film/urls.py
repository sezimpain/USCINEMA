from django.urls import path, include

from rest_framework.routers import DefaultRouter

import account
from .views import VideoViewSet
router = DefaultRouter()

router.register('film', VideoViewSet)

urlpatterns = [
    path('', include(router.urls)),

]
