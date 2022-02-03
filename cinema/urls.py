from django.conf.urls.static import static
from django.contrib import admin

import account
from cinema import settings
from cinema.settings import MEDIA_ROOT
from film.views import CategoryListView, VideoViewSet, VideoPlayView, VideoReviewViewSet
from django.urls import path, include

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('films', VideoViewSet),
router.register('reviews', VideoReviewViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/categories/', CategoryListView.as_view()),
    path('api/v1/add-video/', VideoPlayView.as_view()),
    path('api/v1/', include(router.urls)),
    path('api/v1/', include('account.urls')),
] + static(settings.MEDIA_URL, document_root=MEDIA_ROOT)
