from django.db.models import Q
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from film.models import Video, Category, VideoPlay, VideoReview
from film.serializers import VideoSerializer, CategorySerializer, VideoPlaySerializer, VideoReviewSerializer

from django_filters.rest_framework import DjangoFilterBackend
from .service import FilmFilter


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny, ]



class MyPaginationClass(PageNumberPagination):
    # page_size = 3
    def get_paginated_response(self, data):
        for i in range(self.page_size):
            description = data[i]['description']
            data[i]['description'] = description[:3] + '...'
        return super().get_paginated_response(data)


class VideoViewSet(ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    pagination_class = MyPaginationClass
    permission_classes = [IsAuthenticated, ]

    filter_backends = (DjangoFilterBackend,)
    filterset_class = FilmFilter

    @action(detail=False, methods=['get'])
    def search(self, request, pk=None):
        q = request.query_params.get('q')
        queryset = self.queryset
        queryset = queryset.filter(Q(title__icontains=q) |
                                   Q(description__icontains=q))
        serializer = VideoSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


    def get_serializer_context(self):
        return {
            "request": self.request
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    @action(['GET'], detail=True)
    def reviews(self, request, pk=None):
        product = self.get_object()
        reviews = product.reviews.all()
        serializer = VideoReviewSerializer(
            reviews, many=True, context={'request': request}
        )
        return Response(serializer.data, status=200)

class VideoPlayView(generics.ListCreateAPIView):
    queryset = VideoPlay.objects.all()
    serializer_class = VideoPlaySerializer
    def get_serializer_context(self):
        return {'request':self.request}


class VideoReviewViewSet(ModelViewSet):
    queryset = VideoReview.objects.all()
    serializer_class = VideoReviewSerializer
    # permission_classes = [IsActivePermission]

    def get_serializer_context(self):
        return {
            'request': self.request
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)