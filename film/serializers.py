from django.db.models import Avg
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from film.models import *


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class VideoSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = CategorySerializer(instance.category).data
        representation['rating'] = VideoReview.objects.all().aggregate(Avg('rating'))
        representation['video'] = VideoPlaySerializer(instance.videos.all(), context=self.context, many=True).data
        return representation

class VideoPlaySerializer(ModelSerializer):
    class Meta:
        model = VideoPlay
        fields = '__all__'


class VideoReviewSerializer(ModelSerializer):
    video_title = serializers.SerializerMethodField("get_video_title")
    rating = serializers.IntegerField()

    class Meta:
        model = VideoReview
        fields = "__all__"

    def get_video_title(self, video_review):
        title = video_review.video.title
        return title



    def validate_video(self, video):

        if self.Meta.model.objects.filter(video=video).exists():
            raise serializers.ValidationError(
                "Вы уже оставляли отзыв на этот продукт"
            )
        return video

    def validate_rating(self, rating):
        if rating not in range(1, 6):
            raise serializers.ValidationError(
                "Рейтинг должен быть от 1 до 5"
            )
        return rating

    def create(self, validated_data):
        user = self.context.get('request').user
        validated_data['author'] = user
        review = VideoReview.objects.create(**validated_data)
        return review