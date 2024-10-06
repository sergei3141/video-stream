from rest_framework import serializers
from .models import VideoUpload

class VideoUploadInitSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoUpload
        fields = ['id', 'file_name', 'file_size', 'mime_type', 'user', 'group_id', 'total_chunks']

class VideoChunkUploadSerializer(serializers.Serializer):
    chunk_index = serializers.IntegerField()
    chunk = serializers.FileField()

class VideoChunkCompleteSerializer(serializers.Serializer):
    status = serializers.JSONField()
    file_url = serializers.URLField()