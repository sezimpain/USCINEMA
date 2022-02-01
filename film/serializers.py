from rest_framework.serializers import ModelSerializer

from film.models import Video


class VideoSerializer(ModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"
