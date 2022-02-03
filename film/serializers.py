from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from film.models import Video, Category, VideoPlay, VideoReview


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
        representation['category'] =CategorySerializer(instance.category).data
        representation['video'] = VideoPlaySerializer(instance.videos.all(), context=self.context, many=True).data
        return representation

class VideoPlaySerializer(ModelSerializer):
    class Meta:
        model = VideoPlay
        fields = '__all__'


class VideoReviewSerializer(ModelSerializer):
    video_title = serializers.SerializerMethodField("get_video_title")

    class Meta:
        model = VideoReview
        fields = "__all__"

    def get_video_title(self, product_review):
        title = product_review.video.title
        return title

    def validate_product(self, product):
        # "title": "Edited", "price": 199.99 ...
        # ProductReview.objects.filter(product=product).exists()
        if self.Meta.model.objects.filter(product=product).exists():
            raise serializers.ValidationError(
                "Вы уже оставляли отзыв на этот продукт"
            )
        return product

        # SELECT * FROM a WHERE title = 'hello'

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
