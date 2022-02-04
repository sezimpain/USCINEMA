from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.conf.urls.static import static
from django.contrib import admin
from cinema import settings
from cinema.settings import MEDIA_ROOT
from film.views import CategoryListView, VideoViewSet, VideoPlayView, VideoReviewViewSet
from django.urls import path, include

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('films', VideoViewSet),
router.register('reviews', VideoReviewViewSet)

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api/v1/categories/', CategoryListView.as_view()),
    path('api/v1/add-video/', VideoPlayView.as_view()),
    path('api/v1/', include(router.urls)),
    path('api/v1/', include('account.urls')),
] + static(settings.MEDIA_URL, document_root=MEDIA_ROOT)

